# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaz2.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
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
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
# secure socket layers
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from PyQt5.QtCore import QThreadPool, QRunnable
from Worker import Worker

# theme
from qt_material import apply_stylesheet



# metodo de Alan para crear senales
class WorkerSignals(QtCore.QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal()
    result = QtCore.pyqtSignal(dict)
    progress = QtCore.pyqtSignal(object)

# example from TDS for QRunnable
class Runnable(QRunnable):
    def __init__(self, arg1):
        super().__init__()
        self.arg1 = arg1
        self.signals = WorkerSignals()
        
    def run(self):
        try:
            autotest.run_pySRM(path=self.arg1)
        except:
            # pass
            self.signals.error.emit()
        else:
            pass
            # self.signals.result.emit()  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Ui_MainWindow(object):
    global path_actual
    path_actual = os.getcwd()
    def setupUi(self, MainWindow):
        # crear thread pool
        # self.threadpool1 = QThreadPool()
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1299, 825)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.label_icon_CNR = QtWidgets.QLabel(self.centralwidget)
        self.label_icon_CNR.setMaximumSize(QtCore.QSize(131, 141))
        self.label_icon_CNR.setText("")
        self.label_icon_CNR.setPixmap(QtGui.QPixmap("thumbnails/logotipo-CNR.png"))
        self.label_icon_CNR.setScaledContents(True)
        self.label_icon_CNR.setObjectName("label_icon_CNR")
        self.verticalLayout_5.addWidget(self.label_icon_CNR)
        self.label_programadopor = QtWidgets.QLabel(self.centralwidget)
        self.label_programadopor.setObjectName("label_programadopor")
        self.verticalLayout_5.addWidget(self.label_programadopor)
        self.label_icon_CIREN = QtWidgets.QLabel(self.centralwidget)
        self.label_icon_CIREN.setMaximumSize(QtCore.QSize(121, 51))
        self.label_icon_CIREN.setText("")
        self.label_icon_CIREN.setPixmap(QtGui.QPixmap("thumbnails/logo_CIREN_trans.png"))
        self.label_icon_CIREN.setScaledContents(True)
        self.label_icon_CIREN.setObjectName("label_icon_CIREN")
        self.verticalLayout_5.addWidget(self.label_icon_CIREN)
        self.label_version = QtWidgets.QLabel(self.centralwidget)
        self.label_version.setObjectName("label_version")
        self.verticalLayout_5.addWidget(self.label_version)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_paso1 = QtWidgets.QLabel(self.centralwidget)
        self.label_paso1.setWordWrap(True)
        self.label_paso1.setObjectName("label_paso1")
        self.verticalLayout_4.addWidget(self.label_paso1)
        self.comboBox_cuencas = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cuencas.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_cuencas.setObjectName("comboBox_cuencas")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.comboBox_cuencas.addItem("")
        self.verticalLayout_4.addWidget(self.comboBox_cuencas)
        self.label_paso2 = QtWidgets.QLabel(self.centralwidget)
        self.label_paso2.setWordWrap(True)
        self.label_paso2.setObjectName("label_paso2")
        self.verticalLayout_4.addWidget(self.label_paso2)
        self.comboBox_cuencas_cabecera = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_cuencas_cabecera.setObjectName("comboBox_cuencas_cabecera")
        self.verticalLayout_4.addWidget(self.comboBox_cuencas_cabecera)
        self.label_paso3 = QtWidgets.QLabel(self.centralwidget)
        self.label_paso3.setWordWrap(True)
        self.label_paso3.setObjectName("label_paso3")
        self.verticalLayout_4.addWidget(self.label_paso3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_simular = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_simular.setObjectName("pushButton_simular")
        self.horizontalLayout_3.addWidget(self.pushButton_simular)
        self.pushButton_plotear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_plotear.setObjectName("pushButton_plotear")
        self.horizontalLayout_3.addWidget(self.pushButton_plotear)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.verticalLayout_6.addWidget(self.webEngineView)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_7.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1299, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.comboBox_cuencas.activated.connect(self.seleccionar_cuenca)
        self.comboBox_cuencas_cabecera.currentTextChanged.connect(self.seleccionar_subcuenca)
        self.pushButton_simular.clicked.connect(self.simular_Qrunnable)
        self.pushButton_plotear.clicked.connect(self.plotear_resultados)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MODELO PRONOSTICO CAUDALES CNR"))
        self.label_2.setText(_translate("MainWindow", "MODELO DE PRONOSTICO DE CAUDALES CNR"))
        self.label.setText(_translate("MainWindow", "Preparado para:"))
        self.label_programadopor.setText(_translate("MainWindow", "Programado por:"))
        self.label_version.setText(_translate("MainWindow", "Versión 1.0"))
        self.label_paso1.setText(_translate("MainWindow", "<html><head/><body><p>Paso 1</p><p>Seleccione una macrocuenca del menu desplegable (ej: Río Maipo)</p><p>De esta manera el segundo menú desplegable habilitará las subcuencas correspondientes para su estudio</p></body></html>"))
        self.comboBox_cuencas.setItemText(0, _translate("MainWindow", "<Seleccione una cuenca>"))
        self.comboBox_cuencas.setItemText(1, _translate("MainWindow", "Rio Maipo"))
        self.comboBox_cuencas.setItemText(2, _translate("MainWindow", "Rio Rapel"))
        self.comboBox_cuencas.setItemText(3, _translate("MainWindow", "Rio Mataquito"))
        self.comboBox_cuencas.setItemText(4, _translate("MainWindow", "Rio Maule"))
        self.label_paso2.setText(_translate("MainWindow", "<html><head/><body><p>Paso 2</p><p>Seleccione una subcuenca del menu desplegable (ej: Maipo en El Manzano)</p><p>El mapa explorador a su derecha le mostrara un Google Maps donde podra ubicar la cuenca seleccionada</p></body></html>"))
        self.label_paso3.setText(_translate("MainWindow", "<html><head/><body><p>Paso 3</p><p>Una vez seleccionada la subcuenca el modelo estará listo para simular la próxima temporada de riego o visualizar los resultados si es que éstos ya fueron generados anteriormente</p></body></html>"))
        self.pushButton_simular.setText(_translate("MainWindow", "SIMULAR\n"
"PROXIMA\n"
"TEMPORADA"))
        self.pushButton_plotear.setText(_translate("MainWindow", "VER\n"
"RESULTADOS\n"
"DE MODELACION"))
        
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
            html_subcuenca = os.path.join(path_actual,'basemaps', var_aux.dic_paths[current_subcuenca][-1] + '.html')
            with open(html_subcuenca, 'r') as f:
                html = f.read()
                self.webEngineView.setHtml(html)
                print(html_subcuenca)
                self.webEngineView.show()
            
    def simular(self):
        current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
        path_subcuenca = os.path.join(*var_aux.dic_paths[current_subcuenca])
        path_completo = os.path.join(os.getcwd(),path_subcuenca)
        print('Simulando en: ', path_completo)
        self.pushButton_simular.setEnabled(False)
        self.mensaje_iniciar_simulacion()
        worker = Worker(autotest.run_pySRM, path_completo, tipo = 'P')
        # worker.run()
        # worker.signals.error.connect(self.error)
        worker.signals.result.connect(self.mensaje_simulacion_terminada) # funcion para cuando termina
        
    def simular_Qrunnable(self):
        current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
        path_subcuenca = os.path.join(*var_aux.dic_paths[current_subcuenca])
        path_completo = os.path.join(os.getcwd(),path_subcuenca)
        
        print('Simulando en: ', path_completo)
        self.pushButton_simular.setEnabled(False)
        self.mensaje_iniciar_simulacion()
        
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool().globalInstance()
        runnable = Runnable(path_completo)
        pool.start(runnable)
        # runnable.signals.error.connect(self.mensaje_error_simulacion)
        runnable.signals.finished.connect(self.mensaje_simulacion_terminada)
        
    
    def mensaje_iniciar_simulacion(self):
        current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        texto = 'La simulación se realizará en cuenca:\n' + current_subcuenca\
            + '\nPresione OK para comenzar'
        msg.setText(texto)
        msg.exec_()

    def mensaje_error_simulacion(self):
        errormsg = QMessageBox()
        errormsg.setIcon(QMessageBox.Critical)
        errormsg.setText("Error en la simulación")
        errormsg.exec_()
        self.pushButton_simular.setEnabled(True)
    
    
    def mensaje_simulacion_terminada(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Simulación exitosa")
        msg.exec_()
        self.pushButton_simular.setEnabled(True)
        
        
        # worker.signals.progress.connect(self.progress_fn) #
        
        
        
        
        # try:
            
        #     autotest.run_pySRM(path_completo, tipo = 'P')
        
        #     msg.exec_()
        #     os.chdir(path_actual)
        # except:
        #
        #     print('Error en la simulacion. Volviendo a menu principal')
        #     os.chdir(path_actual)
        
    def plotear_resultados(self):
        plt.close('all')
        current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
        path_subcuenca = os.path.join(*var_aux.dic_paths[current_subcuenca])
        path_completo = os.path.join(os.getcwd(),path_subcuenca)
        path_resultados = os.path.join(path_completo,'SRM','Resultados')
        sufijo = var_aux.dic_paths[current_subcuenca][1]

        print(path_resultados)
        files = [x for x in os.listdir(path_resultados) if (x.startswith("Qsim_")) & (x.endswith(".csv"))]
        files_parsed = [os.path.join(path_resultados,x) for x in files]
        path_caudal_simulado = max(files_parsed, key = os.path.getctime)
        # path_caudal_simulado = os.path.join(path_resultados,
        #                                     'Qsim_'+sufijo+'.csv')
        print(path_caudal_simulado)
        
        try:    
            
            #######################################
            #   graficar periodo de validación    #
            #######################################
    
            #plot settings 
            plot_ini = '2000-01-01'
        
            # cargar el master y su información
            master = pd.read_csv(os.path.join(path_completo,'SRM','Inputs',r'Master.csv'), index_col = 0, parse_dates = True)
                    
 
            #######################################
            #         graficar predictivo         #
            #######################################
            
            years = [x.year for x in master.index]
            years = list(dict.fromkeys(years))
            years = [x for x in years if str(x) != 'nan']
            plot_ini = pd.to_datetime(str(years[-2])+'-04-01')
    
            # Qforecast
            Qfor = pd.read_csv(path_caudal_simulado,
                                             index_col=0,
                                             parse_dates=True, header = 0)
            Qfor = Qfor.loc[Qfor.index >= plot_ini]
            
            # fechas
            Days_xticks = [ x for x in pd.date_range(plot_ini,pd.to_datetime(plot_ini)+datetime.timedelta(days=len(Qfor)-1), freq = '1d').date]  
            last_year = Days_xticks[-1].year 
            first_year = Days_xticks[0].year 
            
            # formatear fechas
            # myFmt = mdates.DateFormatter('%d-%m-%Y')
                                
            # plot relative runoffs
            fig = plt.figure(figsize=(18 , 12))
            ax = fig.add_subplot(2,1,1)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
            ax.plot(Qfor.index, Qfor.values, color='red', linewidth = 2)
            ax.autoscale(enable=True, axis='x', tight=True)
            
            
            ax.set_ylim(bottom = 0)
            ax.set_ylabel('Caudal $(m^3/s)$', fontsize = 12)
            title = 'Pronóstico de caudales para años: ' \
                +str(first_year)+'-'+str(last_year)
            current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
            ax.set_title('\n'.join([title, current_subcuenca]))
            plt.legend(['Q Simulado'])
            _ = plt.xlabel('')
            plt.grid()
                         
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
            axis.autoscale(enable=True, axis='x', tight=True)
            path_caudal_simulado_fig = os.path.join(path_resultados,
                                            'Qsim_'+sufijo+'.jpg')
            plt.savefig(path_caudal_simulado_fig, format='jpg')
            msg_fig_save = QMessageBox()
            msg_fig_save.setIcon(QMessageBox.Information)
            msg_fig_save.setText("Gráfico guardado en\n"\
                                 + path_caudal_simulado_fig)
            msg_fig_save.exec_()
            
        except:
            errormsg = QMessageBox()
            errormsg.setIcon(QMessageBox.Critical)
            errormsg.setText("Error en la carga de resultados\n" \
                             "Simule primero la cuenca o seleccione otra cuenca")
            errormsg.exec_()
        
        
from PyQt5 import QtWebEngineWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
