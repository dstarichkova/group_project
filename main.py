import sys

from PyQt5 import uic

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

import parse_requests

SCREEN_SIZE = [400, 400]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        uic.loadUi('main.ui', self)

    def initUI(self):
        self.setGeometry(400, 400, *SCREEN_SIZE)
        self.setWindowTitle('Отображение картинки')

        parse_requests.update_image([37.637432, 55.752301])

        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.move(250, 250)
        self.image.resize(400, 400)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
