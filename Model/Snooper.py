from Model.Cache import CacheBlockStates
from Model.MemoryRequest import RequestTypes, MemoryRequest


class Snooper:
    def __init__(self, cache=None, memory_bus=None, app=None):
        self.current_block = None  # None means not waiting for data
        self.cache = cache
        self.memory_bus = memory_bus
        self.identifier = None
        self.app = app
        if memory_bus is not None:
            memory_bus.subscribe(self)
        self.action = ""

    def connect_cache(self, cache):
        self.cache = cache

    def connect_bus(self, memory_bus):
        self.memory_bus = memory_bus
        memory_bus.subscribe(self)

    def set_processor(self, identifier):
        self.identifier = identifier

    def flush_write_back(self, cache_block):
        if cache_block is None:
            return
        elif cache_block.coherence_state == CacheBlockStates.OWNED or \
                cache_block.coherence_state == CacheBlockStates.MODIFIED:
            request = MemoryRequest()
            request.type = RequestTypes.FLUSH_WRITE_BACK
            request.data = cache_block.data
            request.address = cache_block.address
            self.memory_bus.post(request)

    def process(self, request):
        cache_block = self.cache.get_block(request.address)
        block_coherence_state = cache_block.coherence_state
        if request.type == RequestTypes.PROCESSOR_READ:
            if block_coherence_state == CacheBlockStates.INVALID:
                self.app.miss(self.identifier)
                request.type = RequestTypes.BUS_READ
                response = self.memory_bus.post(request)
                cache_block.data = response.data
                cache_block.address = request.address
                if response.copies_exist:
                    cache_block.coherence_state = CacheBlockStates.SHARED
                else:
                    cache_block.coherence_state = CacheBlockStates.EXCLUSIVE
            else:
                self.app.hit(self.identifier)
            # All other states (MOES) imply a cache hit
            self.cache.put_block(cache_block)
            return
        elif request.type == RequestTypes.PROCESSOR_WRITE:
            if block_coherence_state == CacheBlockStates.INVALID:
                self.app.miss(self.identifier)
                request.type = RequestTypes.BUS_READ_EXCLUSIVE
                self.memory_bus.post(request)
                cache_block.data = request.data
                cache_block.address = request.address
                cache_block.coherence_state = CacheBlockStates.MODIFIED
                original = self.cache.put_block(cache_block)
                self.flush_write_back(original)
                return
            elif block_coherence_state == CacheBlockStates.SHARED or \
                    block_coherence_state == CacheBlockStates.OWNED:
                self.app.hit(self.identifier)
                request.type = RequestTypes.BUS_UPGRADE
                self.memory_bus.post(request)
            self.app.hit(self.identifier)
            cache_block.coherence_state = CacheBlockStates.MODIFIED
            cache_block.data = request.data
            original = self.cache.put_block(cache_block)
            self.flush_write_back(original)
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
        if block_coherence_state == CacheBlockStates.INVALID or request.type == RequestTypes.RESPONSE:
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
