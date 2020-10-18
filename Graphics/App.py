from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QAbstractItemView, QTableWidgetItem, QHBoxLayout, \
    QGridLayout, QGroupBox, QHeaderView, QLabel


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
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.init_cache_view()
        self.init_cache_view()
        self.init_cache_view()
        self.init_cache_view()

        self.init_memory_view()
        self.layout.addWidget(QLabel(" "), 7, 0, -1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("test"), 0, 0, -1, 1, Qt.AlignVCenter)
        self.layout.addWidget(QLabel("Memory View"), 0, 3, 1, -1, Qt.AlignCenter)
        self.layout.addWidget(self.memory_view, 1, 3, 6, 1, Qt.AlignHCenter)

        self.layout.addWidget(QLabel("Cache View"), 0, 1, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 1"), 1, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 2"), 1, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 3"), 4, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(QLabel("Processor: 4"), 4, 2, 1, 1, Qt.AlignCenter)

        self.layout.addWidget(self.cache_views[0], 3, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[1], 3, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[2], 6, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[3], 6, 2, 1, 1, Qt.AlignCenter)

        self.set_instruction("P0: CALC", 1)
        self.set_instruction("P0: CALC", 2)
        self.set_instruction("P0: CALC", 3)
        self.set_instruction("P0: CALC", 4)
        self.layout.addWidget(QLabel("Instructions View"), 0, 0, 1, 1, Qt.AlignCenter)

        self.setLayout(self.layout)

        # Show widget
        self.show()

    def set_instruction(self, instruction, processor):
        i = 2
        j = 1
        if processor == 1:
            self.layout.addWidget(QLabel(instruction), i, j, 1, 1, Qt.AlignCenter)
        elif processor == 2:
            self.layout.addWidget(QLabel(instruction), i, j + 1, 1, 1, Qt.AlignCenter)
        elif processor == 3:
            self.layout.addWidget(QLabel(instruction), i + 3, j, 1, 1, Qt.AlignCenter)
        elif processor == 4:
            self.layout.addWidget(QLabel(instruction), i + 3, j + 1, 1, 1, Qt.AlignCenter)

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
