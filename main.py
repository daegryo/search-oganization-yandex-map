from PyQt5 import uic
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('des.ui', self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Window()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
