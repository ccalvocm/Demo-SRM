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

folder = os.path.join('.','01_Maipo','01_RMELA','Nieve')
yrs = check_download_MODIS.main(folder)

for yr in yrs:
    nasa_new_win.Prepare_MODIS(folder,yr)

