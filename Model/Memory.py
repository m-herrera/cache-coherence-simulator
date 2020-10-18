import time


class Memory:

    # block_size is specified in bytes
    def __init__(self, latency, num_blocks=16, block_size=2):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.latency = latency
        self.content = [0] * num_blocks

    def __str__(self):
        return str(self.content)

    # TODO: Handle errors
    def write(self, address, data):
        print("Writing memory contents at address: " + str(address))
        if address >= self.num_blocks:
            print("Write error: Address out of range")
        time.sleep(self.latency)
        self.content[address] = data

    # TODO: Handle errors
    def read(self, address):
        print("Reading memory contents at address: " + str(address))
        if address >= self.num_blocks:
            print("Read error: Address out of range")
        time.sleep(self.latency)
        return self.content[address]
