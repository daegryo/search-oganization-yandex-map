from PyQt5 import uic
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from geocode import Gecode
from urllib import request
import os


geo = Gecode('Москва')
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('des.ui', self)
        self.pixmap = QPixmap('image.png')
        self.card_Label.setPixmap(self.pixmap)
        self.searchButton.clicked.connect(self.search)
        self.reset_button.clicked.connect(self.reset)

    def search(self):
        object = self.zapros_lineEdit.text()
        map = geo.one_point(object)
        print(map)
        data = request.urlopen(map).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.card_Label.setPixmap(pixmap)

    def reset(self):
        self.pixmap = QPixmap('image.png')
        self.card_Label.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Window()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
