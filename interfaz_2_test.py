from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5 import QtWebEngineWidgets
import sys
import os

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThreadPool, QRunnable

import interfaz_variables_metodos_auxiliares as var_aux
import autotest
import create_HTMLmaps

# secure socket layers
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from PyQt5.QtCore import QThreadPool, QRunnable
from Worker import Worker


# theme
from qt_material import apply_stylesheet
from autotest_Qrunnable import Runnable_autotest

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
        # self.pushButton_simular.clicked.connect(self.simular_Qrunnable)
        self.pushButton_simular.clicked.connect(self.run_autotest)
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

    def run_autotest(self):
        import check_download_MODIS
        import nasa_new_win
        import process_MODIS
        import snowGlacierCoveredArea
        import create_master_SRM
        import pyCSRM

        current_subcuenca = self.comboBox_cuencas_cabecera.currentText()
        path_subcuenca = os.path.join(*var_aux.dic_paths[current_subcuenca])
        path_completo = os.path.join(os.getcwd(), path_subcuenca)
        path = path_completo

        print('Simulando en: ', path_completo)
        self.pushButton_simular.setEnabled(False)
        self.mensaje_iniciar_simulacion()

        folder = path_completo

        print('Iniciando actualización de imágenes MODIS')
        self.progressBar.setValue(0)
        yrs = check_download_MODIS.main(folder)
        self.progressBar.setValue(1)
        for yr in yrs:
            # reproyectar
            print('Reproyectando nuevas imágenes MODIS')
            try:
                nasa_new_win.Prepare_MODIS(folder, yr)
            except:
                print('Imágenes reproyectadas')

        self.progressBar.setValue(2)
        process_MODIS.main(folder)
        self.progressBar.setValue(3)
        print('Calculando la fracción cubierta nival')
        snowGlacierCoveredArea.main(folder)
        self.progressBar.setValue(4)
        print('Realizando proyección de nieve')
        create_master_SRM.SRM_master(folder)
        self.progressBar.setValue(5)
        print('Iniciando la simulación')
        pyCSRM.DEVELOP_SRM(folder, type_='P', alpha=0.959, Tcrit=1)
        self.progressBar.setValue(6)
        parent_dir = os.path.abspath(os.path.join(path, '..', '..'))
        os.chdir(parent_dir)
        print('Simulacion finalizada exitosamente')



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
    # create_HTMLmaps.renew_html_maps()
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
