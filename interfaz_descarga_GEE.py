# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaz_descarga_GEE.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import import_from_GEE
from import_from_GEE import dic_productos, dataset, dataset_description
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import geopandas as gpd
from matplotlib import pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import ee
service_account = 'srmearthenginelogin@srmlogin.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, '.\\interfaz_descarga_GEE\\srmlogin-175106b08655.json')
ee.Initialize(credentials)

class Ui_widget_test(object):
    def setupUi(self, widget_test):
        widget_test.setObjectName("widget_test")
        widget_test.resize(1014, 897)
        self.centralwidget = QtWidgets.QWidget(widget_test)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_datasets = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_datasets.setGeometry(QtCore.QRect(230, 90, 171, 31))
        self.comboBox_datasets.setObjectName("comboBox_datasets")
        self.comboBox_datasets.addItem("")
        self.comboBox_datasets.addItem("")
        self.comboBox_datasets.addItem("")
        self.comboBox_datasets.addItem("")
        self.comboBox_datasets.addItem("")
        self.comboBox_datasets.addItem("")
        self.comboBox_datasets.addItem("")
        self.comboBox_datasets.addItem("")
        self.label_Select_Producto = QtWidgets.QLabel(self.centralwidget)
        self.label_Select_Producto.setGeometry(QtCore.QRect(10, 90, 231, 31))
        self.label_Select_Producto.setObjectName("label_Select_Producto")
        self.label_Producto_descripcion = QtWidgets.QLabel(self.centralwidget)
        self.label_Producto_descripcion.setGeometry(QtCore.QRect(180, 140, 231, 251))
        self.label_Producto_descripcion.setScaledContents(True)
        self.label_Producto_descripcion.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_Producto_descripcion.setWordWrap(True)
        self.label_Producto_descripcion.setObjectName("label_Producto_descripcion")
        self.label_Preview_Producto = QtWidgets.QLabel(self.centralwidget)
        self.label_Preview_Producto.setGeometry(QtCore.QRect(10, 140, 151, 161))
        self.label_Preview_Producto.setText("")
        self.label_Preview_Producto.setPixmap(QtGui.QPixmap("interfaz_descarga_GEE/thumbnails/google_logo.png"))
        self.label_Preview_Producto.setScaledContents(True)
        self.label_Preview_Producto.setObjectName("label_Preview_Producto")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(630, 90, 201, 31))
        self.label.setObjectName("label")
        self.calendarWidget_1 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget_1.setGeometry(QtCore.QRect(440, 140, 261, 161))
        self.calendarWidget_1.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendarWidget_1.setMaximumDate(QtCore.QDate(2060, 12, 31))
        self.calendarWidget_1.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendarWidget_1.setGridVisible(True)
        self.calendarWidget_1.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget_1.setObjectName("calendarWidget_1")
        self.calendarWidget_2 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget_2.setGeometry(QtCore.QRect(720, 140, 261, 161))
        self.calendarWidget_2.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendarWidget_2.setMaximumDate(QtCore.QDate(2060, 12, 31))
        self.calendarWidget_2.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendarWidget_2.setGridVisible(True)
        self.calendarWidget_2.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget_2.setObjectName("calendarWidget_2")
        self.label_fecha1 = QtWidgets.QLabel(self.centralwidget)
        self.label_fecha1.setGeometry(QtCore.QRect(440, 310, 261, 31))
        self.label_fecha1.setObjectName("label_fecha1")
        self.label_fecha2 = QtWidgets.QLabel(self.centralwidget)
        self.label_fecha2.setGeometry(QtCore.QRect(720, 310, 261, 31))
        self.label_fecha2.setObjectName("label_fecha2")
        self.pushButton_descargar = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_descargar.setGeometry(QtCore.QRect(450, 650, 541, 61))
        self.pushButton_descargar.setObjectName("pushButton_descargar")
        self.lineEdit_ruta_CSV = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ruta_CSV.setGeometry(QtCore.QRect(630, 610, 361, 31))
        self.lineEdit_ruta_CSV.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_ruta_CSV.setObjectName("lineEdit_ruta_CSV")
        self.pushButton_ruta_CSV = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ruta_CSV.setGeometry(QtCore.QRect(450, 610, 171, 31))
        self.pushButton_ruta_CSV.setObjectName("pushButton_ruta_CSV")
        self.label_logo_CIREN = QtWidgets.QLabel(self.centralwidget)
        self.label_logo_CIREN.setGeometry(QtCore.QRect(0, 0, 181, 81))
        self.label_logo_CIREN.setText("")
        self.label_logo_CIREN.setPixmap(QtGui.QPixmap("interfaz_descarga_GEE/thumbnails/logo_CIREN_trans.png"))
        self.label_logo_CIREN.setScaledContents(True)
        self.label_logo_CIREN.setObjectName("label_logo_CIREN")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 0, 781, 91))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.MplWidget = MplWidget(self.centralwidget)
        self.MplWidget.setGeometry(QtCore.QRect(40, 560, 371, 241))
        self.MplWidget.setObjectName("MplWidget")
        self.pushButton_load_shapefile = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_load_shapefile.setGeometry(QtCore.QRect(40, 520, 171, 31))
        self.pushButton_load_shapefile.setObjectName("pushButton_load_shapefile")
        self.label_Variable_descargar = QtWidgets.QLabel(self.centralwidget)
        self.label_Variable_descargar.setGeometry(QtCore.QRect(180, 390, 171, 31))
        self.label_Variable_descargar.setObjectName("label_Variable_descargar")
        self.comboBox_Variables = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Variables.setGeometry(QtCore.QRect(180, 420, 231, 31))
        self.comboBox_Variables.setObjectName("comboBox_Variables")
        self.lineEdit_ruta_shp = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ruta_shp.setGeometry(QtCore.QRect(220, 520, 191, 31))
        self.lineEdit_ruta_shp.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_ruta_shp.setObjectName("lineEdit_ruta_shp")
        self.label_autores = QtWidgets.QLabel(self.centralwidget)
        self.label_autores.setGeometry(QtCore.QRect(840, 730, 171, 71))
        self.label_autores.setObjectName("label_autores")
        widget_test.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(widget_test)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1014, 20))
        self.menubar.setObjectName("menubar")
        widget_test.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(widget_test)
        self.statusbar.setObjectName("statusbar")
        widget_test.setStatusBar(self.statusbar)

        self.pushButton_load_shapefile.clicked.connect(self.define_shp_path)
        self.pushButton_ruta_CSV.clicked.connect(self.define_CSV_path)
        self.comboBox_datasets.activated.connect(self.create_Class)
        self.calendarWidget_1.clicked.connect(self.set_date1)
        self.calendarWidget_2.clicked.connect(self.set_date2)
        self.pushButton_descargar.clicked.connect(self.download)

        self.retranslateUi(widget_test)
        QtCore.QMetaObject.connectSlotsByName(widget_test)

    def retranslateUi(self, widget_test):
        _translate = QtCore.QCoreApplication.translate
        widget_test.setWindowTitle(_translate("widget_test", "CIREN GEE Downloader"))
        self.comboBox_datasets.setToolTip(_translate("widget_test", "Selecciona un producto de Google Earth Engine"))
        self.comboBox_datasets.setItemText(0, _translate("widget_test", "Seleccione un producto"))
        self.comboBox_datasets.setItemText(1, _translate("widget_test", "CFSV2"))
        self.comboBox_datasets.setItemText(2, _translate("widget_test", "CHIRPS"))
        self.comboBox_datasets.setItemText(3, _translate("widget_test", "ERA5_daily"))
        self.comboBox_datasets.setItemText(4, _translate("widget_test", "ERA5_hourly"))
        self.comboBox_datasets.setItemText(5, _translate("widget_test", "GLDAS_2_1"))
        self.comboBox_datasets.setItemText(6, _translate("widget_test", "GPM"))
        self.comboBox_datasets.setItemText(7, _translate("widget_test", "PERSIANN"))
        self.label_Select_Producto.setText(_translate("widget_test", "Seleccione producto meteorologico"))
        self.label_Producto_descripcion.setText(_translate("widget_test", "Breve descripcion del producto"))
        self.label.setText(_translate("widget_test", "Seleccione rango de fechas"))
        self.label_fecha1.setText(_translate("widget_test", "Fecha inicio: "))
        self.label_fecha2.setText(_translate("widget_test", "Fecha fin: "))
        self.pushButton_descargar.setText(_translate("widget_test", "INICIAR DESCARGA"))
        self.lineEdit_ruta_CSV.setText(_translate("widget_test", "Ruta Archivo"))
        self.pushButton_ruta_CSV.setText(_translate("widget_test", "Guardar archivo como..."))
        self.label_2.setText(_translate("widget_test", "Google Earth Engine Downloader by CIREN"))
        self.pushButton_load_shapefile.setText(_translate("widget_test", "Cargar shapefile (.shp)"))
        self.label_Variable_descargar.setText(_translate("widget_test", "Variable a descargar"))
        self.lineEdit_ruta_shp.setText(_translate("widget_test", "Ruta shapefile"))
        self.label_autores.setText(_translate("widget_test", "<html><head/><body><p>version 1.0</p><p>Created by F.A.A</p><p>Sep, 2021</p></body></html>"))


    global aux_str_fecha1
    global aux_str_fecha2

    def define_shp_path(self):
        # self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes.clear()
        aux_FileName_shp = QFileDialog.getOpenFileName(filter="geometry Files (*.shp *.SHP *.geojson)")[0]
        self.lineEdit_ruta_shp.setText(aux_FileName_shp)

        global aux_geodataframe
        aux_geodataframe = gpd.read_file(aux_FileName_shp)
        aux_geodataframe.plot(ax = self.MplWidget.canvas.axes)
        self.MplWidget.canvas.axes.set_title('Vista previa capa')
        self.MplWidget.canvas.draw()

    def define_CSV_path(self):
        aux_FileName = QFileDialog.getSaveFileName(filter="CSV Files (*.csv *.CSV)")[0]
        self.lineEdit_ruta_CSV.setText(aux_FileName)

    def create_Class(self):
        if self.comboBox_datasets.currentText() != 'Seleccione un producto':
            
            aux_producto = self.comboBox_datasets.currentText()

            connection = dataset(dic_productos[aux_producto])

            aux_preview_path = connection.img_preview
            self.label_Preview_Producto.setPixmap(QtGui.QPixmap(aux_preview_path))

            aux_str_descripcion = dataset_description(connection)
            self.label_Producto_descripcion.setText(aux_str_descripcion)

            aux_str_date1 = connection.dates[0]
            aux_str_date2 = connection.dates[1]

            aux_str_fecha1 = aux_str_date1
            aux_str_fecha2 = aux_str_date2

            Qtdate1 = QtCore.QDate.fromString(aux_str_date1, "yyyy-MM-dd")
            Qtdate2 = QtCore.QDate.fromString(aux_str_date2, "yyyy-MM-dd")
            self.calendarWidget_1.setSelectedDate(Qtdate1)
            self.calendarWidget_2.setSelectedDate(Qtdate2)

            self.label_fecha1.setText('Fecha inicio: ' + aux_str_fecha1)
            self.label_fecha2.setText('Fecha fin: ' + aux_str_fecha2)

            # Introducir contenidos al combobox de variables
            self.comboBox_Variables.clear()

            for item in connection.variables.items():
                self.comboBox_Variables.addItem(item[1])


            print(connection.snippet)

    def download(self):
        aux_str_fecha1 = self.calendarWidget_1.selectedDate().toString("yyyy-MM-dd")
        aux_str_fecha2 = self.calendarWidget_2.selectedDate().toString("yyyy-MM-dd")
        gdf = import_from_GEE.catchment_gdf_TS_2(aux_geodataframe,
            self.comboBox_datasets.currentText(),
            self.comboBox_Variables.currentText(),
            aux_str_fecha1,
            aux_str_fecha2,
            simplify=0.3)
        ee.Initialize(credentials)
        gdf.to_csv(self.lineEdit_ruta_CSV.text())
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Serie de tiempo descargada exitosamente")
        
        msg.exec_()



    def set_date1(self):
        aux_str_fecha1 = self.calendarWidget_1.selectedDate().toString("yyyy-MM-dd")
        self.label_fecha1.setText('Fecha inicio: ' + aux_str_fecha1)

    def set_date2(self):
        aux_str_fecha2 = self.calendarWidget_2.selectedDate().toString("yyyy-MM-dd")
        self.label_fecha2.setText('Fecha fin: ' + aux_str_fecha2)

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget_test = QtWidgets.QMainWindow()
    ui = Ui_widget_test()
    ui.setupUi(widget_test)
    widget_test.show()
    sys.exit(app.exec_())

