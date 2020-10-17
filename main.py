from Model.Processor import *
from Model.Memory import *
from Model.Cache import *


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

    cache = Cache(2)
    print(cache)


if __name__ == "__main__":
    main()
