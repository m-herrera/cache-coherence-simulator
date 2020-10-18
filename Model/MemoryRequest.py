from enum import Enum


class MemoryRequest:
    def __init__(self):
        self.type = RequestTypes.NULL
        self.address = None
        self.data = None
        self.copies_exist = False


class RequestTypes(Enum):
    PROCESSOR_READ = 0
    PROCESSOR_WRITE = 1
    BUS_READ = 2
    BUS_READ_EXCLUSIVE = 3  # equivalent of a bus write
    BUS_UPGRADE = 4
    FLUSH = 5
    FLUSH_OPT = 6
    FLUSH_WRITE_BACK = 7
    RESPONSE = 8
    NULL = 9
