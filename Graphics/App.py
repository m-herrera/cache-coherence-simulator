import threading
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QTableWidgetItem, \
    QGridLayout, QHeaderView, QLabel, QPushButton, QLineEdit

from Model.MemoryRequest import RequestTypes

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

        self.lock1_button = QPushButton("lock")
        self.lock2_button = QPushButton("lock")
        self.lock3_button = QPushButton("lock")
        self.lock4_button = QPushButton("lock")

        self.steps = QLineEdit()

        self.bus = QLabel(" ")

        self.processors = []
        self.caches = []
        self.instructions = [None, None, None, None]
        self.hits = [QLabel(), QLabel(), QLabel(), QLabel()]
        self.next_instructions = [None, None, None, None]
        self.memory = None
        self.threads = []
        self.locks = [False, False, False, False]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.init_cache_view()
        self.init_cache_view()
        self.init_cache_view()
        self.init_cache_view()

        self.init_memory_view()
        self.layout.addWidget(QLabel("BUS TRANSACTION:"), 10, 1, -1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.bus, 10, 2, -1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel(" "), 11, 1, -1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel(" "), 0, 0, 1, -1, Qt.AlignCenter)
        self.layout.addWidget(QLabel(" "), 0, 5, 1, -1, Qt.AlignCenter)
        self.layout.addWidget(QLabel(" "), 0, 7, 1, -1, Qt.AlignCenter)
        mem_view_label = QLabel("Memory View")
        mem_view_label.setStyleSheet("font-size:15pt; font-weight:600; color:#000000;")
        self.layout.addWidget(mem_view_label, 0, 6, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.memory_view, 1, 6, 9, 1, Qt.AlignHCenter)

        processor_view_label = QLabel("Processor View")
        processor_view_label.setStyleSheet("font-size:15pt; font-weight:600; color:#000000;")
        self.layout.addWidget(processor_view_label, 0, 1, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 0"), 2, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 1"), 2, 3, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 2"), 6, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 3"), 6, 3, 1, 1, Qt.AlignCenter)

        self.layout.addWidget(self.cache_views[0], 5, 1, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[1], 5, 3, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[2], 9, 1, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[3], 9, 3, 1, 2, Qt.AlignCenter)

        self.layout.addWidget(self.step_button, 1, 1, alignment=Qt.AlignCenter)
        self.step_button.setMinimumWidth(175)
        self.step_button.clicked.connect(lambda: self.step())

        self.layout.addWidget(self.exec_button, 1, 2, 1, 1, alignment=Qt.AlignCenter)
        self.exec_button.setMinimumWidth(175)
        self.exec_button.clicked.connect(lambda: self.thread_execute())

        self.layout.addWidget(self.steps, 1, 3, 1, 1, alignment=Qt.AlignCenter)
        self.steps.setMinimumWidth(175)
        self.steps.setPlaceholderText("Steps")
        self.steps.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.pause_button, 1, 4, alignment=Qt.AlignCenter)
        self.pause_button.clicked.connect(lambda: self.pause_execution())
        self.pause_button.setMinimumWidth(175)

        self.layout.addWidget(self.lock1_button, 2, 2, alignment=Qt.AlignCenter)
        self.lock1_button.clicked.connect(lambda: self.lock(1))
        self.layout.addWidget(self.lock2_button, 2, 4, alignment=Qt.AlignCenter)
        self.lock2_button.clicked.connect(lambda: self.lock(2))
        self.layout.addWidget(self.lock3_button, 6, 2, alignment=Qt.AlignCenter)
        self.lock3_button.clicked.connect(lambda: self.lock(3))
        self.layout.addWidget(self.lock4_button, 6, 4, alignment=Qt.AlignCenter)
        self.lock4_button.clicked.connect(lambda: self.lock(4))

        self.layout.addWidget(self.hits[0], 3, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.hits[1], 3, 4, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.hits[2], 7, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.hits[3], 7, 4, 1, 1, Qt.AlignCenter)

        self.setLayout(self.layout)
        self.show()

    def lock(self, index):
        self.locks[index - 1] = not self.locks[index - 1]
        color = "light gray"
        if self.locks[index - 1]:
            color = "red"
        if index == 1:
            self.lock1_button.setStyleSheet("background-color:" + color)
        elif index == 2:
            self.lock2_button.setStyleSheet("background-color:" + color)
        elif index == 3:
            self.lock3_button.setStyleSheet("background-color:" + color)
        elif index == 4:
            self.lock4_button.setStyleSheet("background-color:" + color)

    def thread_execute(self):
        # self.execute()
        thread = threading.Thread(target=self.execute, daemon=True)
        thread.start()

    def execute(self):
        global execution
        if execution:
            return
        execution = True
        try:
            steps = int(self.steps.text())
            for i in range(steps):
                self.step()
                time.sleep(1)
                self.steps.setText(str(steps - 1 - i))
                self.steps.update()
        except:
            while True:
                if not execution:
                    break
                self.step()
                time.sleep(1)
        self.steps.setText("")
        execution = False

    def pause_execution(self):
        global execution
        execution = False

    def step(self):
        i = 0
        self.memory.tick()
        for processor in self.processors:
            if processor.busy or len(processor.instructions) == 0 or self.locks[i]:
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
            for hit in self.hits:
                hit.setText("")

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
        i = 3
        j = 1
        self.next_instructions[processor - 1] = QLineEdit(instruction)
        self.next_instructions[processor - 1].setMinimumWidth(250)
        self.next_instructions[processor - 1].setAlignment(Qt.AlignCenter)

        self.instructions[processor - 1] = QLabel(instruction)
        if processor == 1:
            self.layout.addWidget(self.instructions[processor - 1], i, j, 1, 1, Qt.AlignCenter)
            self.layout.addWidget(self.next_instructions[processor - 1], i + 1, j, 1, 2, Qt.AlignCenter)

        elif processor == 2:
            self.layout.addWidget(self.instructions[processor - 1], i, j + 2, 1, 1, Qt.AlignCenter)
            self.layout.addWidget(self.next_instructions[processor - 1], i + 1, j + 2, 1, 2, Qt.AlignCenter)
        elif processor == 3:
            self.layout.addWidget(self.instructions[processor - 1], i + 4, j, 1, 1, Qt.AlignCenter)
            self.layout.addWidget(self.next_instructions[processor - 1], i + 5, j, 1, 2, Qt.AlignCenter)
        elif processor == 4:
            self.layout.addWidget(self.instructions[processor - 1], i + 4, j + 2, 1, 1, Qt.AlignCenter)
            self.layout.addWidget(self.next_instructions[processor - 1], i + 5, j + 2, 1, 2, Qt.AlignCenter)

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
        self.memory_view.update()

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

    def hit(self, processor):
        try:
            i = int(processor[1])
            self.hits[i].setText("HIT")
            self.hits[i].update()
        except:
            print("hit by " + processor)

    def miss(self, processor):
        try:
            i = int(processor[1])
            self.hits[i].setText("MISS")
            self.hits[i].update()
        except:
            print("miss by " + processor)

    def set_bus(self, request):
        if request != RequestTypes.RESPONSE:
            self.bus.setText(request.name)
