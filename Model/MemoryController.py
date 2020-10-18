from Model.MemoryRequest import *


class MemoryController:
    def __init__(self, memory=None, memory_bus=None):
        self.memory = memory
        self.memory_bus = memory_bus

    def connect_memory(self, memory):
        self.memory = memory

    def connect_bus(self, memory_bus):
        self.memory_bus = memory_bus
        memory_bus.connect_memory_controller(self)

    def notify(self, request):
        response = MemoryRequest()
        if request.type == RequestTypes.BUS_READ:
            response.data = self.memory.read(request.address)
            response.type = RequestTypes.RESPONSE
            response.address = request.address
        elif request.type == RequestTypes.FLUSH_WRITE_BACK:
            self.memory.write(request.address, request.data)
            response.type = RequestTypes.NULL
        return response
