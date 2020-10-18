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
    memory_bus = MemoryBus()
    memory = Memory(0)
    memory_controller = MemoryController()
    memory_controller.connect_memory(memory)
    memory_controller.connect_bus(memory_bus)
    ex.update_memory_view(memory)
    cache1 = Cache(0)
    snooper1 = Snooper()
    snooper1.connect_cache(cache1)
    snooper1.connect_bus(memory_bus)

    processor = Processor("P0", 9, snooper=snooper1)
    processor.load_instructions(50)
    # processor.execute()
    ex.update_memory_view(memory)
    ex.update_cache_view(cache1, 0)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
