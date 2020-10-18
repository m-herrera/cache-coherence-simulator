from Model.MemoryBus import MemoryBus
from Model.MemoryController import MemoryController
from Model.Processor import *
from Model.Memory import *
from Model.Cache import *
from Model.Snooper import Snooper


def main():
    # processor = Processor("P0", 9)
    # processor.load_instructions(100)
    # for inst in processor.instructions:
    #     print(inst)
    # memory = Memory(3)
    # print(memory)
    # memory.write(0, 3)
    # print(memory)
    # print(memory.read(1))
    # print(memory.read(0))

    memory_bus = MemoryBus()
    memory = Memory(0)
    memory_controller = MemoryController()
    memory_controller.connect_memory(memory)
    memory_controller.connect_bus(memory_bus)
    print(memory)

    cache1 = Cache(0)
    snooper1 = Snooper()
    snooper1.connect_cache(cache1)
    snooper1.connect_bus(memory_bus)

    processor = Processor("P0", 9, snooper=snooper1)
    processor.load_instructions(50)
    processor.execute()
    print(memory)
    # cache2 = Cache(2)
    # snooper2 = Snooper()
    # snooper2.connect_cache(cache2)
    # snooper2.connect_bus(memory_bus)
    #
    # cache3 = Cache(2)
    # snooper3 = Snooper()
    # snooper3.connect_cache(cache3)
    # snooper3.connect_bus(memory_bus)
    #
    # cache4 = Cache(2)
    # snooper4 = Snooper()
    # snooper4.connect_cache(cache4)
    # snooper4.connect_bus(memory_bus)
    # memory_bus.connect_memory_controller(memory_controller)


if __name__ == "__main__":
    main()
