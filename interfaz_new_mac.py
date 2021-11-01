from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from menu import Menu
import sys



class Main:
    def __init__(self):
        self.stack = QStackedWidget()
        self.stack.addWidget(Menu(self))

        self.stack.setCurrentIndex(0)
        self.stack.show()


if __name__ == "__main__":

    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    my_gui = Main()
    app.exec()
