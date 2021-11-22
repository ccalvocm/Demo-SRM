from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5 import QtWebEngineWidgets
import sys
import os

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThreadPool, QRunnable

import interfaz_variables_metodos_auxiliares as var_aux
import autotest

# secure socket layers
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from PyQt5.QtCore import QThreadPool, QRunnable
from Worker import Worker


# theme
from qt_material import apply_stylesheet


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





class Ui_MainWindow(QtWidgets.QMainWindow):
    global path_actual
    path_actual = os.getcwd()

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        uic.loadUi('interfaz.ui', self)

        self.comboBox_cuencas.activated.connect(self.seleccionar_cuenca)
        self.comboBox_cuencas_cabecera.currentTextChanged.connect(self.seleccionar_subcuenca)
        self.pushButton_simular.clicked.connect(self.simular_Qrunnable)
        # self.pushButton_plotear.clicked.connect(self.plotear_resultados)


        self.show()

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
            html_subcuenca = os.path.join(path_actual, 'basemaps', var_aux.dic_paths[current_subcuenca][-1] + '.html')
            with open(html_subcuenca, 'r') as f:
                html = f.read()
                self.webEngineView.setHtml(html)
                print(html_subcuenca)
                self.webEngineView.show()

    def simular_Qrunnable(self):
        current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
        path_subcuenca = os.path.join(*var_aux.dic_paths[current_subcuenca])
        path_completo = os.path.join(os.getcwd(), path_subcuenca)

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
        texto = 'La simulación se realizará en cuenca:\n' + current_subcuenca \
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
