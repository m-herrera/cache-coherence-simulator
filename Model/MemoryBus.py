from Model.MemoryRequest import *
from threading import Lock


class MemoryBus:
    def __init__(self):
        self.busy = False
        self.request = None
        self.listeners = []
        self.memory_controller = None
        self.lock = Lock()

    def post(self, request):
        # must return a response for the snooper
        with self.lock:
            response = MemoryRequest()
            for listener in self.listeners:
                temp_response = listener.notify(request)
                response.copies_exist = response.copies_exist or temp_response.copies_exist
                if temp_response.type == RequestTypes.FLUSH or temp_response.type == RequestTypes.FLUSH_OPT:
                    response.data = temp_response.data
                    response.address = temp_response.address
                    response.type = temp_response.type
                elif temp_response.type != RequestTypes.NULL:
                    self.post(temp_response)
            if response.type == RequestTypes.NULL:
                response = self.memory_controller.notify(request)
            return response

    def connect_memory_controller(self, memory_controller):
        self.memory_controller = memory_controller

    def subscribe(self, listener):
        self.listeners.append(listener)
        return
