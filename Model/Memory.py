import time


class Memory:

    # block_size is specified in bytes
    def __init__(self, latency, num_blocks=16, block_size=2):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.latency = latency
        self.ticks = 0
        self.content = [0] * num_blocks

    def __str__(self):
        return str(self.content)

    def tick(self):
        self.ticks += 1

    def write(self, address, data):
        self.ticks = 0
        if address >= self.num_blocks:
            print("Write error: Address out of range")
        while self.ticks < self.latency:
            continue
        self.ticks = 0
        print(address)
        self.content[address] = data

    def read(self, address):
        self.ticks = 0
        if address >= self.num_blocks:
            print("Read error: Address out of range")
        while self.ticks < self.latency:
            continue
        self.ticks = 0
        return self.content[address]
