import copy
from enum import Enum


class Cache:

    # block_size is specified in bytes
    def __init__(self, latency, num_blocks=4, block_size=2, associativity=2):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.latency = latency
        self.associativity = associativity
        sets = num_blocks // associativity
        self.content = []
        temp = []
        id = 0
        for i in range(sets):
            for j in range(associativity):
                temp.append(CacheBlock(id))
                id += 1
            self.content.append(temp)
            temp = []

    def __str__(self):
        result = ""
        for cache_set in self.content:
            for cache_block in cache_set:
                result += cache_block.__str__() + "\n"
        return result

    def get_item(self, index):
        for cache_set in self.content:
            for cache_block in cache_set:
                if cache_block.identifier == index:
                    return cache_block.get_address_str(), cache_block.get_data_str(), cache_block.coherence_state.name

        return None, None

    def get_block(self, address):
        _set = self.content[address % (self.num_blocks // self.associativity)]
        for cache_block in _set:
            hit = cache_block.address == address
            if hit:
                return cache_block
        return CacheBlock(-1)

    def put_block(self, cache_block):
        _set = self.content[cache_block.address % (self.num_blocks // self.associativity)]
        for block in _set:
            hit = block.address == cache_block.address
            if hit:
                block.data = cache_block.data
                _set.insert(0, _set.pop(_set.index(block)))  # Update for LRU policy
                return None

        to_replace = _set[-1]
        original = copy.deepcopy(to_replace)
        to_replace.address = cache_block.address
        to_replace.data = cache_block.data
        to_replace.coherence_state = cache_block.coherence_state
        _set.insert(0, _set.pop(-1))  # Write in position for LRU
        return original


class CacheBlockStates(Enum):
    MODIFIED = 0
    OWNED = 1
    EXCLUSIVE = 2
    SHARED = 3
    INVALID = 4


class CacheBlock:
    def __init__(self, identifier, coherence_state=CacheBlockStates.INVALID, data=0, address=0):
        self.identifier = identifier
        self.coherence_state = coherence_state
        self.data = data
        self.address = address

    def get_data_str(self):
        return '0x' + '{:04x}'.format(self.data).upper()

    def get_address_str(self):
        return '{:04b}'.format(self.address)

    def __str__(self):
        return str(self.identifier) + ": (" + self.coherence_state.name[
            0] + ") " + self.get_address_str() + " " + self.get_data_str()
