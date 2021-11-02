# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 12:44:25 2021

@author: ccalvo
"""

import pandas as pd
import os
from subprocess import Popen
from os.path import isfile, join

def list_out(directory):
    files = [f for f in os.listdir(directory) if (isfile(join(directory, f))) & (f.endswith('.out'))]
    return files


def main():
    
    # rutas
    path_unc_in = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\01_RMELA\SRM\Inputs\unc_analysis.in'
    path_master = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\01_RMELA\SRM\Inputs\Master.pst'
    
    path_unc_in = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\02_RMEEM\SRM\Inputs\unc_analysis.in'
    path_master = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\02_RMEEM\SRM\Inputs\Master.pst'    


    unc_in = pd.read_csv(path_unc_in)
    
    # Río Mapocho en Los Almendros
    master = pd.read_csv(path_master, skiprows = 7618, nrows=365, sep = '\t', header = None, index_col = 0)
    # Río Maipo en el Manzano
    master = pd.read_csv(path_master, skiprows = 7356, nrows=365, sep = ' ', header = None, index_col = 1)
    
    # ruta de archivos de simulacion
    # folder = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\01_RMELA\SRM\Inputs'
    folder = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\02_RMEEM\SRM\Inputs'
    
    # iterar sobre caudales
    for caudal in master.index:
        # guardar el archivo de análisis de incertidumbre
        caudal = caudal.strip()
        unc_in.loc[3] = 'linear_uncer_'+caudal+'.out'
        
        # reemplazar prediccion
        unc_in.loc[5] = caudal
        
        # guardar
        unc_in.to_csv(path_unc_in, index = None)
    
        # ejecutar el análisis de incertidumbre
        # ruta_bat = r"C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\01_RMELA\SRM\Inputs"
        ruta_bat = folder
        p = Popen("run_uncert.bat", cwd=ruta_bat)
        p.communicate()

    # juntar las desviaciones estandar
    listout = list_out(folder)
    listout.sort()
    
    # lista de desviaciones estandar
    lista_std_dev = []
    
    # leer las desviaciones estandar
    for file in listout:
        file_read = pd.read_csv(os.path.join(folder,file))
        # std_dev = float(file_read.loc[173].values[0].split('=')[-1].split()[0])
        std_dev = float(file_read.loc[196].values[0].split('=')[-1].split()[0])
        lista_std_dev.append(std_dev)
    
    df_std_dev = pd.DataFrame(lista_std_dev, columns = ['Desviacion estandar (l/s)'])
    df_std_dev.index = pd.date_range(pd.to_datetime('2021-04-01'),pd.to_datetime('2022-03-31'),freq = '1d')
    df_std_dev.to_csv(os.path.join(folder,'df_std_dev.csv'))
       
        
if __name__ == '__main__':
    main()