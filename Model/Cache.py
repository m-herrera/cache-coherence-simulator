import time
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

    # TODO: Handle errors and add Replacement policy
    def write(self, address, data):
        if data >= self.block_size * 255:
            print("Write error: Data too big")
        time.sleep(self.latency)
        set = self.content[address % (self.num_blocks // self.associativity)]
        for cache_block in set:
            hit = cache_block.address == address
            if hit:
                print("Hit")
                cache_block.data = data
                set.insert(0, set.pop(set.index(cache_block)))  # Update for LRU policy
                return cache_block
        set[-1].address = address
        set[-1].data = data
        set.insert(0, set.pop(-1))  # Write in position for LRU

    # TODO: Handle errors and add Replacement policy
    def read(self, address):
        print("Searching address in cache")
        time.sleep(self.latency)
        set = self.content[address % (self.num_blocks // self.associativity)]
        for cache_block in set:
            hit = cache_block.address == address
            if hit:
                print("Hit")
                set.insert(0, set.pop(set.index(cache_block)))  # Update for LRU policy
                return cache_block

        print("Miss")
        return None

    def get_block(self):
        return

    def put_block(self):
        return


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
