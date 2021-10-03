# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaz.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import interfaz_variables_metodos_auxiliares as var_aux
import os
import autotest
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pandas as pd
from matplotlib import pyplot as plt
import datetime
import numpy as np


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_cuencas = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cuencas.setGeometry(QtCore.QRect(10, 90, 231, 21))
        self.comboBox_cuencas.setObjectName("comboBox_cuencas")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas_cabecera = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cuencas_cabecera.setGeometry(QtCore.QRect(10, 120, 231, 22))
        self.comboBox_cuencas_cabecera.setObjectName("comboBox_cuencas_cabecera")
        self.pushButton_simular = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_simular.setGeometry(QtCore.QRect(260, 400, 111, 61))
        self.pushButton_simular.setObjectName("pushButton_simular")
        self.pushButton_plotear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_plotear.setGeometry(QtCore.QRect(420, 400, 111, 61))
        self.pushButton_plotear.setObjectName("pushButton_plotear")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.comboBox_cuencas.activated.connect(self.seleccionar_cuenca)
        self.comboBox_cuencas_cabecera.currentTextChanged.connect(self.seleccionar_subcuenca)
        self.pushButton_simular.clicked.connect(self.simular)
        self.pushButton_plotear.clicked.connect(self.plotear_resultados)

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
        self.pushButton_simular.setText(_translate("MainWindow", "SIMULAR\n"
"PROXIMA\n"
"TEMPORADA"))
        self.pushButton_plotear.setText(_translate("MainWindow", "PLOTEAR\n"
"RESULTADOS"))
        
        
    global path_subcuenca

    def seleccionar_cuenca(self):
        
        if self.comboBox_cuencas.currentText() != "<Seleccione una cuenca>":
            opcion = self.comboBox_cuencas.currentText()
            self.comboBox_cuencas_cabecera.clear()
            for item in var_aux.dic_cuencas[opcion]:
                self.comboBox_cuencas_cabecera.addItem(item)
                
    def seleccionar_subcuenca(self):
        if self.comboBox_cuencas_cabecera.currentText() != '':    
            current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
            path_subcuenca = os.path.join(*var_aux.dic_paths[current_subcuenca])
            print(path_subcuenca)
            
    def simular(self):
        current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
        path_subcuenca = os.path.join(*var_aux.dic_paths[current_subcuenca])
        path_completo = os.path.join(os.getcwd(),path_subcuenca)
        print(path_completo)
        try:
            autotest.run_pySRM(path_completo, tipo = 'P')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Simulación exitosa")
        except:
            errormsg = QMessageBox()
            errormsg.setIcon(QMessageBox.Critical)
            errormsg.setText("Error en la simulación")
            
    def plotear_resultados(self):
        current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
        path_subcuenca = os.path.join(*var_aux.dic_paths[current_subcuenca])
        path_completo = os.path.join(os.getcwd(),path_subcuenca)
        path_resultados = os.path.join(path_completo,'SRM','Resultados')
        sufijo = var_aux.dic_paths[current_subcuenca][1]
        print(sufijo)
        path_caudal_simulado = os.path.join(path_resultados,
                                            'Qsim_'+sufijo+'.csv')
        print(path_caudal_simulado)
        df_caudal_simulado = pd.read_csv(path_caudal_simulado,
                                         header = None,
                                         index_col=0,
                                         parse_dates=True)
        
         # graficar predictivo
          # cargar el master y su información
        master = pd.read_csv(os.path.join(path_completo,'SRM','Inputs',r'Master.csv'), index_col = 0, parse_dates = True)
        
        # leer precipitaciones
        Pbands = master[[x for x in master.columns if 'Pp_z' in x]]
        
        # leer temperaturas
        Tbands = master[[x for x in master.columns if 'T_z' in x]] 
        
        # leer curva hipsométrica
        ruta_hipso = os.path.join(path_completo,'SRM','Inputs',r'Hypso.csv')
        Area = pd.read_csv(ruta_hipso, index_col = 0)['area'].values
        
        years = [x.year for x in master.index]
        years = list(dict.fromkeys(years))
        plot_ini = pd.to_datetime(str(years[-2])+'-04-01')
    
        # Qactual
        Qactual = master['Measured Discharge'] # Actual flow (m3/s)
        Qactual = Qactual.loc[Qactual.index >= plot_ini]/1e3
            
        # Qforecast
        Qfor = pd.read_csv(os.path.join(path_completo,'SRM','Resultados',r'Qsim_01_RMELA.csv'), index_col = 0, parse_dates = True, header = None)
        Qfor = Qfor.loc[Qfor.index >= plot_ini]/1e3
        
        # fechas
        Days_xticks = [ x for x in pd.date_range(plot_ini,pd.to_datetime(plot_ini)+datetime.timedelta(days=len(Qfor)-1), freq = '1d').date]  
        
        rot = 15
        last_year = Days_xticks[-1].year 
        first_year = Days_xticks[0].year 
        
        # find the limits of the plots to properly scale the data
        # precpitaci�n y temperatura promedio
        Pmean=1000*np.sum(Pbands*Area, axis = 1)/np.sum(Area)
        Tmean=np.sum(Tbands*Area, axis = 1) / np.sum(Area)
    
        Pmean = pd.DataFrame(Pmean, index = master.index)
        Pmean = Pmean.loc[Pmean.index >= plot_ini]        
    
        Tmean = pd.DataFrame(Tmean, index = master.index)
        Tmean = Tmean.loc[Tmean.index >= plot_ini]    
        
        # settings para plots
        frequency = 60
        
        # plot relative runoffs
        Days = range(0,len(Qfor.index))
        fig = plt.figure(figsize=(18 , 12))
        ax = fig.add_subplot(2,1,1)
        plt.plot(Days,Qfor.values,'r-', linewidth = 2)
        plt.ylabel('Caudal $(m^3/s)$', fontsize = 12)
        plt.title('Pronóstico de caudales para años: ' +str(first_year)+'-'+str(last_year))
        plt.legend(['Q Simulado'])
            
        plt.axis([Days[0],Days[-1],0,1.5*max(Qfor.values)])
        plt.grid()
        
        locs, labels = plt.xticks()  # Get the current locations and labels.
        plt.xticks(Days[::frequency], Days_xticks[::frequency], rotation=rot, fontsize = 10)  # Set text labels and properties.
             
        # now actually plot it.
        axis = fig.add_subplot(2,1,2)           
        # calcular los caudales medios mensuales
        Q_mon = Qfor.resample('MS').mean()
        Q_mon.reset_index(inplace = True, drop = True)
        
        # graficar la curva de variación estacional histórica
    
        cve = pd.read_csv(os.path.join(path_completo,'SRM','Inputs',r'CVE.csv'), skiprows = 1)
    
        colores =  ['blue','magenta',  'yellow',  'cyan', 'purple', 'brown']
        
        # curva de variacion estaiconal historica
        cve.plot(ax = axis, color=colores, style='-', markersize=12, legend=False, linewidth = 3, logy=False)
                         
        # caudales medios mensuales pronosticados
        Q_mon.plot(ax = axis, color='r', style='--', marker = 'D', markersize=10, legend=False, linewidth = 3, logy=False)
        
        axis.set_ylabel('Caudal $(m^3/s)$',  fontsize = 12)
        axis.set_ylim(bottom = 0)
        axis.grid(linestyle='-.')
        axis.legend(['Q5%','Q10%', 'Q20%','Q50%','Q85%', 'Q95%','Qpronóstico'], prop={'size': 9})
        axis.set_xticks(range(12)) 
        _ = axis.set_xticklabels(['Abr', 'May', 'Jun ', 'Jul', 'Ago', 'Sep', 'Oct',
                     'Nov', 'Dic', 'Ene', 'Feb', 'Mar'], fontsize = 12)
        plt.show()
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

