# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 16:57:45 2021

@author: ccalvo
"""

# =================================================================
#               snowCover GUI.py script para controlar 
#                       process_MODIS.py  
#                     snowGlacierCoveredArea
# -----------------------------------------------------------------
#               Selección de las MODIS según la cuenca                
# -----------------------------------------------------------------
# Parameters  
# ----------
# dir_in : str
#     directorio donde se encuentran las MODIS reproyectadas.
# shp : str
#     ruta del shape de la cuenca.
# dir_out : str
#     ruta de salida.
# yeari : int
#     año de inicio.
# yearf : int
#     año de término.
# Returns
# -------
# None.

import check_download_MODIS
import os
import nasa_new_win
import process_MODIS
import snowGlacierCoveredArea
import datetime
import create_master_SRM
import pyCSRM
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import ssl

# class Thread(QThread):
#     _signal = pyqtSignal(int)


def run_pySRM(path, tipo = 'P'):
    ssl._create_default_https_context = ssl._create_unverified_context
    folder = os.path.abspath(path)
    print('Iniciando actualización de imágenes MODIS')
    progress = "Inicializando actualizacion de imagenes MODIS"
    # progressbar = QProgressDialog('Modelo en progreso', 'Cancelar', 0, 6)
    # progressbar.setWindowModality(Qt.WindowModal)
    # progressbar.setValue(0)
    
    # msg = QMessageBox()
    # msg.setStandardButtons(QMessageBox.Ok)
    # msg.setDefaultButton(QMessageBox.Ok)
    # buttonOk = msg.button(QMessageBox.Ok)
    # buttonOk.setText('OK')
    # buttonOk.setEnabled(False)
    # msg.setText(progress)
    
    # msg.exec_()
    try:
        yrs = check_download_MODIS.main(folder)
    except:
        yrs=[datetime.date.today().year]
    # Termina proceso check download MODIS
    # progressbar.setValue(1)
    for yr in yrs:
        # reproyectar
        print('Reproyectando nuevas imágenes MODIS')
        try:
            nasa_new_win.Prepare_MODIS(folder,yr)
    
        except:
            print('Imágenes reproyectadas')
        
        process_MODIS.main(folder, yr)
        parent_dir = os.path.abspath(os.path.join(path, '..', '..'))
        os.chdir(parent_dir)
        # Termina proceso Prepare_Modis
        # progressbar.setValue(2)
        # progress = [progress, 'Intersectando MODIS con la subcuenca']
        
        # msg.setText(progress)
        # Termina proceso process_MODIS
        # progressbar.setValue(3)
        print('Calculando la fracción cubierta nival')
        snowGlacierCoveredArea.main(folder, yr)
    # Termina proceso snowGlacierCoveredArea
    # progressbar.setValue(4)
    print('Realizando proyección de nieve')
    create_master_SRM.SRM_master(folder)
    # Termina proceso create_Master
    # progressbar.setValue(5)
    # tipo = 'V' o 'P'
    print('Iniciando la simulación')
    pyCSRM.DEVELOP_SRM(folder, type_ = tipo, alpha = 0.959, Tcrit = 1)
    # Termina proceso DEVELOP_SRM
    # progressbar.setValue(6)
    parent_dir = os.path.abspath(os.path.join(path, '..', '..'))
    os.chdir(parent_dir)
    print('Simulacion finalizada exitosamente')
    

if __name__ == '__main__':
    # directorio de la cuenca
    folder = os.path.abspath(os.path.join('.','01_Maipo','01_RMELA'))
    folder = os.path.abspath(os.path.join('.','04_Maule','01_RMEA'))

    
    run_pySRM(folder, tipo = 'P')
    
    
