class Memory:

    # block_size is specified in bytes
    def __init__(self, latency, num_blocks=16, block_size=2):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.latency = latency
        self.content = [0] * num_blocks

    def __str__(self):
        return self.content
