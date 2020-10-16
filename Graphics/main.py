from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
import sys


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('PyQt5 App')
    window.setGeometry(100, 100, 280, 80)
    window.move(60, 15)
    hello_msg = QLabel('<h1>Hello World!</h1>', parent=window)
    hello_msg.move(60, 15)
    print("Hello World!")

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
