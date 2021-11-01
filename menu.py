from PyQt5 import uic
from PyQt5.QtWidgets import QLabel

ui = uic.loadUiType("./interfaz_mac/interfaz_new_mac.ui")


class Menu(ui[0], ui[1]):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.background = QLabel(self)
        self.background.setMinimumSize(800, 600)
        self.setupUi(self)




