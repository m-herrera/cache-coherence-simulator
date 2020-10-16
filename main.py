from Model.Processor import *


def main():
    processor = Processor("cortexA9", 9)
    processor.load_instructions(100)
    for inst in processor.instructions:
        print(inst)


if __name__ == "__main__":
    main()
