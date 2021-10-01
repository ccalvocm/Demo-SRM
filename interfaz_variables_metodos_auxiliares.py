# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 18:20:16 2021

@author: farrospide
"""

import os

dic_cuencas = {'Rio Maipo': ['Rio Mapocho en Los Almendros',
                         'Rio Maipo en El Manzano'],
               'Rio Rapel': ['Rio Cachapoal en Puente Termas de Cauquenes',
                         'Rio Claro en Hacienda Las Nieves',
                         'Rio Tinguiririca bajo Los Briones'],
               'Rio Mataquito': ['Rio Teno despues de junta con Claro',
                             'Rio Colorado en junta con Palos',
                             'Rio Palos en junta con Colorado'],
               'Rio Maule': ['Rio Maule en Armerillo']}


dic_paths = {'Rio Mapocho en Los Almendros': ['.','01_Maipo','01_RMELA'],
             'Rio Maipo en El Manzano': ['.','01_Maipo','02_RMEEM'],
             'Rio Cachapoal en Puente Termas de Cauquenes': \
                 ['.','02_Rapel','01_RCEPTDC'],
             'Rio Claro en Hacienda Las Nieves': \
                 ['.','02_Rapel','02_RCEHLN'],
             'Rio Tinguiririca bajo Los Briones': \
                 ['.','02_Rapel','03_RTBLB'],
             'Rio Teno despues de junta con Claro': \
                 ['.','03_Mataquito','01_RTDJCC'],
             'Rio Colorado en junta con Palos': \
                 ['.','03_Mataquito','02_RCEJCP'],
             'Rio Palos en junta con Colorado': \
                 ['.','03_Mataquito','02_RPEJCC'],
             'Rio Maule en Armerillo': \
                 ['.','04_Maule','01_RMEA']}



    
if __name__ == '__main__':
    macrocuenca = 'Rio Mataquito'
    subcuenca = dic_cuencas[macrocuenca][2]
    
    path = os.path.join(*dic_paths[subcuenca])
    print(path)