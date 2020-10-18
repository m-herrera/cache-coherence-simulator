from Model.Cache import CacheBlockStates
from Model.MemoryRequest import RequestTypes, MemoryRequest


class Snooper:
    def __init__(self, cache=None, memory_bus=None):
        self.current_block = None  # None means not waiting for data
        self.cache = cache
        self.memory_bus = memory_bus
        self.identifier = None

    def connect_cache(self, cache):
        self.cache = cache

    def connect_bus(self, memory_bus):
        self.memory_bus = memory_bus
        memory_bus.subscribe(self)

    def set_processor(self, identifier):
        self.identifier = identifier

    def process(self, request):
        cache_block = self.cache.get_block(request.address)
        block_coherence_state = cache_block.coherence_state
        if request.type == RequestTypes.PROCESSOR_READ:
            if block_coherence_state == CacheBlockStates.INVALID:
                request.type = RequestTypes.BUS_READ
                response = self.memory_bus.post(request)
                cache_block.data = response.data
                if response.copies_exist:
                    cache_block.coherence_state = CacheBlockStates.SHARED
                else:
                    cache_block.coherence_state = CacheBlockStates.EXCLUSIVE
            # All other states (MOES) imply a cache hit
            return cache_block.data
        elif request.type == RequestTypes.PROCESSOR_WRITE:
            if block_coherence_state == CacheBlockStates.INVALID:
                request.type = RequestTypes.BUS_READ_EXCLUSIVE
                response = self.memory_bus.post(request)
                cache_block.data = response.data
                cache_block.coherence_state = CacheBlockStates.MODIFIED
                return
            elif block_coherence_state == CacheBlockStates.SHARED or \
                    block_coherence_state == CacheBlockStates.OWNED:
                request.type = RequestTypes.BUS_UPGRADE
                self.memory_bus.post(request)
            cache_block.coherence_state = CacheBlockStates.MODIFIED
            cache_block.data = request.data
        else:
            self.memory_bus.post(request)  # Owned replaced

        return None

    def notify(self, request):
        response = MemoryRequest()
        cache_block = self.cache.get_block(request.address)
        block_coherence_state = cache_block.coherence_state
        response.copies_exist = True
        response.address = request.address
        response.type = RequestTypes.RESPONSE
        if block_coherence_state == CacheBlockStates.INVALID:
            response.copies_exist = False
            response.type = RequestTypes.NULL
        elif block_coherence_state == CacheBlockStates.EXCLUSIVE:
            if request.type == RequestTypes.BUS_READ:
                cache_block.coherence_state = CacheBlockStates.SHARED
            elif request.type == RequestTypes.BUS_READ_EXCLUSIVE:
                cache_block.coherence_state = CacheBlockStates.INVALID
            response.type = RequestTypes.FLUSH_OPT
            response.data = cache_block.data
        elif block_coherence_state == CacheBlockStates.SHARED:
            if request.type == RequestTypes.BUS_READ_EXCLUSIVE or \
                    request.type == RequestTypes.BUS_UPGRADE:
                cache_block.coherence_state = CacheBlockStates.INVALID
                response.type = RequestTypes.NULL
        elif block_coherence_state == CacheBlockStates.MODIFIED:
            if request.type == RequestTypes.BUS_READ:
                response.data = cache_block.data
                cache_block.coherence_state = CacheBlockStates.OWNED
            elif request.type == RequestTypes.BUS_READ_EXCLUSIVE:
                cache_block.coherence_state = CacheBlockStates.INVALID
            response.type = RequestTypes.FLUSH
        elif block_coherence_state == CacheBlockStates.OWNED:
            if request.type == RequestTypes.BUS_READ:
                response.type = RequestTypes.FLUSH
                response.data = cache_block.data
            elif request.type == RequestTypes.BUS_READ_EXCLUSIVE:
                response.type = RequestTypes.FLUSH
                response.data = cache_block.data
                cache_block.coherence_state = CacheBlockStates.INVALID
            elif request.type == RequestTypes.BUS_UPGRADE:
                cache_block.coherence_state = CacheBlockStates.INVALID
                response.type = RequestTypes.NULL
        return response
