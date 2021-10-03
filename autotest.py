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

# directorio de la cuenca
folder = os.path.abspath(os.path.join('.','01_Maipo','01_RMELA','Nieve'))

# bajar nieve nueva
yrs = check_download_MODIS.main(folder)

for yr in yrs:
# reproyectar
    nasa_new_win.Prepare_MODIS(folder,yr)

# clipear la nieve
path_cuenca = os.path.join(os.path.split(folder)[0],'shapes','cuenca.shp')
process_MODIS.main(folder,path_cuenca,folder)

# calcular la scf
path_bandas = os.path.join(os.path.split(folder)[0],'shapes','bandas.shp')
path_glaciares = os.path.join(os.path.split(folder)[0],'shapes','glaciares.shp')
snowGlacierCoveredArea.main(path_bandas, path_glaciares, folder, datetime.date.today().year, datetime.date.today().year+1)

# crear master predictivo
path_q = os.path.join(folder.replace('Nieve','Caudales'), 'Caudales.csv')
ruta_n = folder
root = folder.replace('Nieve','SRM')
ruta_pp =  os.path.join(folder.replace('Nieve','Precipitacion'), r'pp.csv')
ruta_t = os.path.join(folder.replace('Nieve','Temperatura'), r't.csv')

create_master_SRM.SRM_master(path_q, ruta_n, root, ruta_pp , ruta_t)
