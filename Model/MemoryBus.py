class MemoryBus:
    def __init__(self):
        self.busy = False
        self.copies_exist = False
        self.request = None
        self.requester = None

    def post(self):
        # must return a response for the snooper
        return

    def subscribe(self, snooper):
        return
