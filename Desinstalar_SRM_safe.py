# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:02:16 2022

@author: ccalvo
"""


import os
os.system('cmd /k call choco uninstall miniconda3')
os.system('cmd /k call CD ..')
os.system('cmd /k call del "%USERPROFILE%\Desktop\CNR-SRM.lnk"')
os.system('cmd /k call del "%USERPROFILE%\Desktop\Actualizar_SRM.lnk"')
os.system('cmd /k call del "%USERPROFILE%\Desktop\interfaz_clima_GEE.lnk"')
os.system('cmd /k call rmdir /s /q %~dp0..\Demo-SRM')






