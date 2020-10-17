from Model.Cache import CacheBlockStates
from Model.MemoryBus import *
from Model.MemoryRequest import RequestTypes


class Snooper:
    def __init__(self, cache=None):
        self.current_block = None  # None means not waiting for data
        self.cache = cache

    def connect_cache(self, cache):
        self.cache = cache

    def connect_bus(self, memory_bus):
        memory_bus.subscribe(self)

    def process(self, request):
        cache_block = self.cache.get_block(request.address)
        block_coherence_state = cache_block.coherence_state
        if request.type == RequestTypes.PROCESSOR_READ:
            if block_coherence_state == CacheBlockStates.INVALID:
                request.type = RequestTypes.BUS_READ
                response = MemoryBus.post(request)
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
                response = MemoryBus.post(request)
                cache_block.data = response.data
                cache_block.coherence_state = CacheBlockStates.MODIFIED
                return
                # self.cache.put_block(cache_block)
            elif block_coherence_state == CacheBlockStates.SHARED or \
                    block_coherence_state == CacheBlockStates.OWNED:
                request.type = RequestTypes.BUS_UPGRADE
                MemoryBus.post(request)
            cache_block.coherence_state = CacheBlockStates.MODIFIED
            cache_block.data = request.data
        else:
            MemoryBus.post(request)  # Owned replaced

        return None

    def notify(self, request):
        cache_block = self.cache.get_block(request.address)
        block_coherence_state = cache_block.coherence_state
        request.copies_exist = True
        if block_coherence_state == CacheBlockStates.INVALID:
            request.copies_exist = False
        elif block_coherence_state == CacheBlockStates.EXCLUSIVE:
            if request.type == RequestTypes.BUS_READ:
                cache_block.coherence_state = CacheBlockStates.SHARED
            elif request.type == RequestTypes.BUS_READ_EXCLUSIVE:
                cache_block.coherence_state = CacheBlockStates.INVALID
            request.type = RequestTypes.FLUSH_OPT
            request.data = cache_block.data
        elif block_coherence_state == CacheBlockStates.SHARED:
            if request.type == RequestTypes.BUS_READ_EXCLUSIVE or \
                    request.type == RequestTypes.BUS_UPGRADE:
                cache_block.coherence_state = CacheBlockStates.INVALID
        elif block_coherence_state == CacheBlockStates.MODIFIED:
            if request.type == RequestTypes.BUS_READ:
                request.data = cache_block.data
                cache_block.coherence_state = CacheBlockStates.OWNED
            elif request.type == RequestTypes.BUS_READ_EXCLUSIVE:
                cache_block.coherence_state = CacheBlockStates.INVALID
            request.type = RequestTypes.FLUSH
        elif block_coherence_state == CacheBlockStates.OWNED:
            if request.type == RequestTypes.BUS_READ:
                request.type = RequestTypes.FLUSH
                request.data = cache_block.data
            elif request.type == RequestTypes.BUS_READ_EXCLUSIVE:
                request.type = RequestTypes.FLUSH
                request.data = cache_block.data
                cache_block.coherence_state = CacheBlockStates.INVALID
            elif request.type == RequestTypes.BUS_UPGRADE:
                cache_block.coherence_state = CacheBlockStates.INVALID
