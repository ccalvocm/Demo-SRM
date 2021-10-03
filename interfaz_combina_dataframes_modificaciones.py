# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaz_combina_dataframes.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
# importar
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pandas as pd

# funcion
def combinar_dataframes(path1, path2):
    df1 = pd.read_csv(path1, index_col=0, parse_dates=(True))
    df2 = pd.read_csv(path2, index_col=0, parse_dates=(True))
    
    df_ext = pd.concat([df1,df2], axis=0)
    df_ext.to_csv(path1[:-4] + '_actualizado.csv')



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_Actual = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Actual.setGeometry(QtCore.QRect(30, 190, 161, 31))
        self.pushButton_Actual.setObjectName("pushButton_Actual")
        self.pushButton_Nueva = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Nueva.setGeometry(QtCore.QRect(30, 230, 161, 31))
        self.pushButton_Nueva.setObjectName("pushButton_Nueva")
        self.label_Actual = QtWidgets.QLabel(self.centralwidget)
        self.label_Actual.setGeometry(QtCore.QRect(200, 190, 231, 31))
        self.label_Actual.setObjectName("label_Actual")
        self.label_Nueva = QtWidgets.QLabel(self.centralwidget)
        self.label_Nueva.setGeometry(QtCore.QRect(200, 230, 201, 31))
        self.label_Nueva.setObjectName("label_Nueva")
        self.pushButton_combinar = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_combinar.setGeometry(QtCore.QRect(30, 280, 231, 31))
        self.pushButton_combinar.setObjectName("pushButton_combinar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # Metodos
        self.pushButton_Actual.clicked.connect(self.define_actual_path)
        self.pushButton_Nueva.clicked.connect(self.define_nueva_path)
        self.pushButton_combinar.clicked.connect(self.combinar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Actual.setText(_translate("MainWindow", "Cargar serie actual"))
        self.pushButton_Nueva.setText(_translate("MainWindow", "Cargar serie nueva"))
        self.label_Actual.setText(_translate("MainWindow", "TextLabel"))
        self.label_Nueva.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_combinar.setText(_translate("MainWindow", "Combinar"))
    
    # funciones
    def define_actual_path(self):
        aux_FileName_actual = QFileDialog.getOpenFileName(filter="csv Files (*.csv *.CSV)")[0]
        self.label_Actual.setText(aux_FileName_actual)
        
    def define_nueva_path(self):
        aux_FileName_nueva = QFileDialog.getOpenFileName(filter="csv Files (*.csv *.CSV)")[0]
        self.label_Nueva.setText(aux_FileName_nueva)
        
    def combinar(self):
        actual = self.label_Actual.text()
        nueva = self.label_Nueva.text()
        combinar_dataframes(actual, nueva)
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

