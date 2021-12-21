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
    # Mapocho en Los Almendros
    path_unc_in = os.path.join('.','01_Maipo','01_RMELA','SRM','LU','unc_analysis.in')
    path_master = os.path.join('.','01_Maipo','01_RMELA','SRM','LU','master_lu.pst')
  
    # Maipo en el Manzano
    # path_unc_in = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\02_RMEEM\SRM\LU\unc_analysis.in'
    # path_master = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\02_RMEEM\SRM\LU\master_lu.pst'    

    # # Río Cachapoal en Puente Termas de Cauquenes
    # path_unc_in = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\02_Rapel\01_RCEPTDC\SRM\Inputs\unc_analysis.in'
    # path_master = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\02_Rapel\01_RCEPTDC\SRM\Inputs\Master.pst'
    
    # # Río Maule en Armerillo
    # path_unc_in = r'D:\GitHub\Demo-SRM\04_Maule\01_RMEA\SRM\LU\unc_analysis.in'
    # path_master = r'D:\GitHub\Demo-SRM\04_Maule\01_RMEA\SRM\LU\master_lu.pst'
    
    # # Río Teno Después de Junta con Claro
    # path_unc_in = r'D:\GitHub\Demo-SRM\03_Mataquito\01_RTDJCC\SRM\LU\unc_analysis.in'
    # path_master = r'D:\GitHub\Demo-SRM\03_Mataquito\01_RTDJCC\SRM\LU\master_lu.pst'    
    
    # Río Claro en Hacienda Las Nieves
    # path_unc_in = os.path.join('.','02_Rapel','02_RCEHLN','SRM','LU','unc_analysis.in')
    # path_master = os.path.join('.','02_Rapel','02_RCEHLN','SRM','LU','master_lu.pst')
    
    # Río Tinguiririca Bajo Los Briones
    # path_unc_in = os.path.join('.','02_Rapel','03_RTBLB','SRM','LU','unc_analysis.in')
    # path_master = os.path.join('.','02_Rapel','03_RTBLB','SRM','LU','master_lu.pst')
    
    # Río Colorado Después de Junta con Claro
    # path_unc_in = os.path.join('.','03_Mataquito','02_RCEJCP','SRM','LU','unc_analysis.in')
    # path_master = os.path.join('.','03_Mataquito','02_RCEJCP','SRM','LU','master_lu.pst')    

    # Río Palos en Junta con Colorado
    # path_unc_in = os.path.join('.','03_Mataquito','03_RPEJCC','SRM','LU','unc_analysis.in')
    # path_master = os.path.join('.','03_Mataquito','03_RPEJCC','SRM','LU','master_lu.pst')   
    
    unc_in = pd.read_csv(path_unc_in)
    
    # Río Mapocho en Los Almendros
    pst = pd.read_csv(path_master, skiprows = 7618, nrows=365, sep = '\t', header = None, index_col = 0)
    # # Río Maipo en el Manzano
    # pst = pd.read_csv(path_master, skiprows = 7356, nrows=365, sep = '\t', header = None, index_col = 0)
    # Río Cachapoal en Puente Termas
    # pst = pd.read_csv(path_master, skiprows = 4198, nrows=365, sep = '\t', header = None, index_col = 0)
    # Río Maule en Armerillo
    # pst = pd.read_csv(path_master, skiprows = 5048, nrows=365, sep = '\t', header = None, index_col = 0)
    # Río Teno Después de Junta con Claro
    # pst = pd.read_csv(path_master, skiprows = 7494, nrows=365, sep = '\t', header = None, index_col = 0)
    # Río Claro en Hacienda Las Nieves
    # pst = pd.read_csv(path_master, skiprows = 6430, nrows=365, sep = '\t', header = None, index_col = 0)
    # Río Tinguiririca Bajo los Briones
    # pst = pd.read_csv(path_master, skiprows = 6804, nrows=365, sep = '\t', header = None, index_col = 0)
    
    # ruta de archivos de simulacion
    # folder = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\01_RMELA\SRM\LU'
    # folder = r'C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\02_RMEEM\SRM\Inputs'
    folder = path_master.replace('master_lu.pst','')
    os.chdir(folder)
        
    # iterar sobre caudales
    idx = [x.strip() for x in pst.index]
    for caudal in idx:
        # guardar el archivo de análisis de incertidumbre
        unc_in.loc[3] = 'linear_uncer_'+caudal+'.out'
        
        # reemplazar prediccion
        unc_in.loc[5] = caudal
        
        # guardar
        unc_in.to_csv('.\\unc_analysis.in', index = None)
    
        # ejecutar el análisis de incertidumbre
        # ruta_bat = r"C:\Users\ccalvo\Documents\GitHub\Demo SRM\Demo-SRM\01_Maipo\01_RMELA\SRM\Inputs"
        ruta_bat = folder
        p = Popen("run_uncert.bat")
        p.communicate()

    # juntar las desviaciones estandar
    listout = list_out('.')
    listout.sort()
    
    # lista de desviaciones estandar
    lista_std_dev = []
    
    # leer las desviaciones estandar
    for file in listout:
        file_read = pd.read_csv(file)
        std_dev = float(file_read.loc[173].values[0].split('=')[-1].split()[0])
        # std_dev = float(file_read.loc[196].values[0].split('=')[-1].split()[0])
        # std_dev = float(file_read.loc[163].values[0].split('=')[-1].split()[0])
        # Río Teno Después de Junta con Claro
        # std_dev = float(file_read.loc[163].values[0].split('=')[-1].split()[0])
        # Río Claro en Hacienda Las Nieves
        # std_dev = float(file_read.loc[144].values[0].split('=')[-1].split()[0])
        # Río Tinguiririca Bajo Los Briones
        # std_dev = float(file_read.loc[168].values[0].split('=')[-1].split()[0])
        # Río Colorado Después de Junta con Claro
        # std_dev = float(file_read.loc[155].values[0].split('=')[-1].split()[0])
        # Río Palos en Junta con Colorado
        # std_dev = float(file_read.loc[139].values[0].split('=')[-1].split()[0])

        lista_std_dev.append(std_dev)
    
    df_std_dev = pd.DataFrame(lista_std_dev, columns = ['Desviacion estandar (l/s)'])
    df_std_dev.index = pd.date_range(pd.to_datetime('2021-04-01'),pd.to_datetime('2022-03-31'),freq = '1d')
    df_std_dev.to_csv(os.path.join('..','Inputs','df_std_dev.csv'))
       
        
if __name__ == '__main__':
    main()