import threading

from Model.MemoryBus import MemoryBus
from Model.MemoryController import MemoryController
from Model.Processor import *
from Model.Memory import *
from Model.Cache import *
from Model.Snooper import Snooper


def main():
    memory_bus = MemoryBus()

    memory = Memory(0)
    memory_controller = MemoryController(memory, memory_bus)

    cache1 = Cache(0)
    cache2 = Cache(0)
    cache3 = Cache(0)
    cache4 = Cache(0)
    snooper1 = Snooper(cache1, memory_bus)
    snooper2 = Snooper(cache2, memory_bus)
    snooper3 = Snooper(cache3, memory_bus)
    snooper4 = Snooper(cache4, memory_bus)

    processor1 = Processor("P0", 9, snooper=snooper1)
    processor2 = Processor("P1", 9, snooper=snooper2)
    processor3 = Processor("P2", 9, snooper=snooper3)
    processor4 = Processor("P3", 9, snooper=snooper4)

    processor1.load_instructions(30)
    processor2.load_instructions(30)
    processor3.load_instructions(30)
    processor4.load_instructions(30)

    t1 = threading.Thread(target=processor1.execute)
    t1.start()
    t2 = threading.Thread(target=processor2.execute)
    t2.start()
    t3 = threading.Thread(target=processor3.execute)
    t3.start()
    t4 = threading.Thread(target=processor4.execute)
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print(cache1)
    print(cache2)
    print(cache3)
    print(cache4)

    print(memory)

if __name__ == "__main__":
    main()
