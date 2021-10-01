# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\interfaz.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import interfaz_variables_metodos_auxiliares as var_aux


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_cuencas = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cuencas.setGeometry(QtCore.QRect(10, 90, 151, 21))
        self.comboBox_cuencas.setObjectName("comboBox_cuencas")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas_cabecera = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cuencas_cabecera.setGeometry(QtCore.QRect(10, 120, 151, 22))
        self.comboBox_cuencas_cabecera.setObjectName("comboBox_cuencas_cabecera")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.comboBox_cuencas.activated.connect(self.seleccionar_cuenca)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox_cuencas.setItemText(0, _translate("MainWindow", "<Seleccione una cuenca>"))
        self.comboBox_cuencas.setItemText(1, _translate("MainWindow", "Rio Maipo"))
        self.comboBox_cuencas.setItemText(2, _translate("MainWindow", "Rio Rapel"))
        self.comboBox_cuencas.setItemText(3, _translate("MainWindow", "Rio Mataquito"))
        self.comboBox_cuencas.setItemText(4, _translate("MainWindow", "Rio Maule"))
        
    def seleccionar_cuenca(self):
        
        if self.comboBox_cuencas.currentText() != "<Seleccione una cuenca>":
            opcion = self.comboBox_cuencas.currentText()
            self.comboBox_cuencas_cabecera.clear()
            for item in var_aux.dic_cuencas[opcion]:
                self.comboBox_cuencas_cabecera.addItem(item)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
