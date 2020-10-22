import threading

from PyQt5.QtWidgets import QApplication
import sys
from Model.MemoryBus import MemoryBus
from Model.MemoryController import MemoryController
from Model.Processor import *
from Model.Memory import *
from Model.Cache import *
from Model.Snooper import Snooper

from Graphics.App import App


def main():
    app = QApplication(sys.argv)
    ex = App()

    memory_bus = MemoryBus(ex)

    memory = Memory(3)
    memory_controller = MemoryController(memory, memory_bus)

    cache1 = Cache(0)
    cache2 = Cache(0)
    cache3 = Cache(0)
    cache4 = Cache(0)
    snooper1 = Snooper(cache1, memory_bus, ex)
    snooper2 = Snooper(cache2, memory_bus, ex)
    snooper3 = Snooper(cache3, memory_bus, ex)
    snooper4 = Snooper(cache4, memory_bus, ex)

    processor1 = Processor("P0", 9, snooper=snooper1)
    processor2 = Processor("P1", 9, snooper=snooper2)
    processor3 = Processor("P2", 9, snooper=snooper3)
    processor4 = Processor("P3", 9, snooper=snooper4)

    processor1.load_instructions(100)
    processor2.load_instructions(100)
    processor3.load_instructions(100)
    processor4.load_instructions(100)

    ex.add_processor(processor1)
    ex.add_processor(processor2)
    ex.add_processor(processor3)
    ex.add_processor(processor4)

    ex.set_memory(memory)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
