import threading
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QTableWidgetItem, \
    QGridLayout, QHeaderView, QLabel, QPushButton, QLineEdit

execution = False


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.memory_view = None
        self.cache_views = []
        self.title = 'Cache Coherence Simulator'
        self.left = 0
        self.top = 0
        self.width = 1080
        self.height = 720
        self.layout = QGridLayout()
        self.step_button = QPushButton("Step")
        self.exec_button = QPushButton("Execute")
        self.pause_button = QPushButton("Pause")
        self.processors = []
        self.caches = []
        self.instructions = [None, None, None, None]
        self.next_instructions = [None, None, None, None]
        self.memory = None
        self.threads = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.init_cache_view()
        self.init_cache_view()
        self.init_cache_view()
        self.init_cache_view()

        self.init_memory_view()
        self.layout.addWidget(QLabel(" "), 9, 0, -1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("test"), 0, 0, -1, 1, Qt.AlignVCenter)
        self.layout.addWidget(QLabel("Memory View"), 0, 3, 1, -1, Qt.AlignCenter)
        self.layout.addWidget(self.memory_view, 1, 3, 8, 1, Qt.AlignHCenter)

        self.layout.addWidget(QLabel("Cache View"), 0, 1, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 0"), 1, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 1"), 1, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 2"), 5, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 3"), 5, 2, 1, 1, Qt.AlignCenter)

        self.layout.addWidget(self.cache_views[0], 4, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[1], 4, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[2], 8, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[3], 8, 2, 1, 1, Qt.AlignCenter)

        self.layout.addWidget(QLabel("Instructions View"), 0, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.step_button, 2, 0)
        self.step_button.clicked.connect(lambda: self.step())
        self.layout.addWidget(self.exec_button, 3, 0)
        self.exec_button.clicked.connect(lambda: self.thread_execute())
        self.layout.addWidget(self.pause_button, 4, 0)
        self.pause_button.clicked.connect(lambda: self.pause_execution())

        self.setLayout(self.layout)
        self.show()

    def thread_execute(self):
        # self.execute()
        thread = threading.Thread(target=self.execute, daemon=True)
        thread.start()

    def execute(self):
        global execution
        if execution:
            return
        execution = True

        while True:
            if not execution:
                break
            self.step()
            time.sleep(1)

    def pause_execution(self):
        global execution
        execution = False

    def exec_step(self):
        if execution:
            return
        self.step()

    def step(self):
        i = 0
        self.memory.tick()
        for processor in self.processors:
            if processor.busy or len(processor.instructions) == 0:
                i += 1
                continue
            if self.instructions[i].text() == "":
                self.next_instructions[i].setText(processor.instructions[0].__str__())
            self.instructions[i].setText(self.next_instructions[i].text())
            if len(processor.instructions) != 1:
                self.next_instructions[i].setText(processor.instructions[1].__str__())
            else:
                processor.load_instructions(100)

            processor.set_next(self.instructions[i].text())
            processor.cycles += 1
            i += 1

        self.update_cache()
        self.update_memory_view(self.memory)

    def add_processor(self, processor):
        self.processors.append(processor)
        self.add_cache(processor.snooper.cache)
        self.set_instruction("", len(self.processors))
        thread = threading.Thread(target=processor.execute, daemon=True)
        thread.start()
        self.threads.append(thread)

    def add_cache(self, cache):
        self.caches.append(cache)
        self.update_cache()

    def set_memory(self, memory):
        self.memory = memory
        self.update_memory_view(self.memory)

    def set_instruction(self, instruction, processor):
        i = 2
        j = 1
        self.next_instructions[processor - 1] = QLineEdit(instruction)
        self.instructions[processor - 1] = QLabel(instruction)
        if processor == 1:
            self.layout.addWidget(self.instructions[processor - 1], i, j, 1, 1, Qt.AlignCenter)
            self.layout.addWidget(self.next_instructions[processor - 1], i + 1, j, 1, 1, Qt.AlignCenter)
        elif processor == 2:
            self.layout.addWidget(self.instructions[processor - 1], i, j + 1, 1, 1, Qt.AlignCenter)
            self.layout.addWidget(self.next_instructions[processor - 1], i + 1, j + 1, 1, 1, Qt.AlignCenter)
        elif processor == 3:
            self.layout.addWidget(self.instructions[processor - 1], i + 4, j, 1, 1, Qt.AlignCenter)
            self.layout.addWidget(self.next_instructions[processor - 1], i + 5, j, 1, 1, Qt.AlignCenter)
        elif processor == 4:
            self.layout.addWidget(self.instructions[processor - 1], i + 4, j + 1, 1, 1, Qt.AlignCenter)
            self.layout.addWidget(self.next_instructions[processor - 1], i + 5, j + 1, 1, 1, Qt.AlignCenter)

    def init_memory_view(self, memory_blocks=16):
        self.memory_view = QTableWidget()
        self.memory_view.setRowCount(memory_blocks)
        self.memory_view.setColumnCount(2)
        for i in range(memory_blocks):
            address = QTableWidgetItem('{:04b}'.format(i))
            address.setTextAlignment(Qt.AlignCenter)
            self.memory_view.setItem(i, 0, address)
        self.memory_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.memory_view.verticalHeader().hide()
        self.memory_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.memory_view.setFocusPolicy(Qt.NoFocus)
        self.memory_view.horizontalHeader().setStretchLastSection(True)
        self.memory_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.memory_view.setHorizontalHeaderLabels(["Address", "Content"])
        self.memory_view.setMinimumWidth(315)

    def update_memory_view(self, memory):
        for i in range(self.memory_view.rowCount()):
            data = QTableWidgetItem('0x' + '{:04x}'.format(memory.content[i]).upper())
            data.setTextAlignment(Qt.AlignCenter)
            self.memory_view.setItem(i, 1, data)

    def init_cache_view(self, cache_blocks=4):
        cache_view = QTableWidget()
        cache_view.setRowCount(cache_blocks)
        cache_view.setColumnCount(3)
        cache_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        cache_view.setHorizontalHeaderLabels(["Address", "Content", "State"])
        cache_view.setSelectionMode(QAbstractItemView.NoSelection)
        cache_view.setFocusPolicy(Qt.NoFocus)
        cache_view.horizontalHeader().setStretchLastSection(True)
        cache_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        cache_view.verticalHeader().setStretchLastSection(True)
        cache_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        cache_view.setMinimumWidth(315)
        self.cache_views.append(cache_view)

    def update_cache(self):
        i = 0
        for cache in self.caches:
            self.update_cache_view(cache, i)
            i += 1

    def update_cache_view(self, cache, index):
        for i in range(self.cache_views[index].rowCount()):
            address = QTableWidgetItem(cache.get_item(i)[0])
            address.setTextAlignment(Qt.AlignCenter)
            self.cache_views[index].setItem(i, 0, address)

            data = QTableWidgetItem(cache.get_item(i)[1])
            data.setTextAlignment(Qt.AlignCenter)
            self.cache_views[index].setItem(i, 1, data)

            data = QTableWidgetItem(cache.get_item(i)[2])
            data.setTextAlignment(Qt.AlignCenter)
            self.cache_views[index].setItem(i, 2, data)
            self.cache_views[index].update()
