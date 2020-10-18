from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QAbstractItemView, QTableWidgetItem, QHBoxLayout, \
    QGridLayout, QGroupBox, QHeaderView


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
        self.init_memory_view()
        self.init_cache_view()
        self.init_cache_view()
        self.init_cache_view()
        self.init_cache_view()

        self.layout.addWidget(self.memory_view, 0, 0, -1, 1)

        self.layout.addWidget(self.cache_views[0], 0, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[1], 0, 2, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[2], 1, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.cache_views[3], 1, 2, 1, 1, Qt.AlignCenter)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def init_memory_view(self, memory_blocks=16):
        self.memory_view = QTableWidget()
        self.memory_view.setRowCount(memory_blocks)
        self.memory_view.setColumnCount(2)
        for i in range(memory_blocks):
            self.memory_view.setItem(i, 0, QTableWidgetItem('{:04b}'.format(i)))
        self.memory_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.memory_view.verticalHeader().hide()
        self.memory_view.setHorizontalHeaderLabels(["Address", "Content"])
        self.memory_view.move(0, 0)

    def update_memory_view(self, memory):
        for i in range(self.memory_view.rowCount()):
            self.memory_view.setItem(i, 1, QTableWidgetItem('0x' + '{:04x}'.format(memory.content[i]).upper()))

    def init_cache_view(self, cache_blocks=4):
        cache_view = QTableWidget()
        cache_view.setRowCount(cache_blocks)
        cache_view.setColumnCount(2)
        cache_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        cache_view.setHorizontalHeaderLabels(["Address", "Content"])
        cache_view.move(0, 0)
        cache_view.setSelectionMode(QAbstractItemView.NoSelection)
        cache_view.setFocusPolicy(Qt.NoFocus)
        cache_view.horizontalHeader().setStretchLastSection(True)
        cache_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        cache_view.verticalHeader().setStretchLastSection(True)
        cache_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cache_views.append(cache_view)

    def update_cache_view(self, cache, index):
        for i in range(self.cache_views[index].rowCount()):
            address = QTableWidgetItem(cache.get_item(i)[0])
            address.setTextAlignment(Qt.AlignCenter)
            self.cache_views[index].setItem(i, 0, address)

            data = QTableWidgetItem(cache.get_item(i)[1])
            data.setTextAlignment(Qt.AlignCenter)
            self.cache_views[index].setItem(i, 1, data)
