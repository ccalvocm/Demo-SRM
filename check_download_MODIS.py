# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 14:04:44 2021

@author: Carlos
"""
import os
from datetime import date
import download_MODIS
from os import listdir
from os.path import isfile, join
import datetime
import calendar

def list_folders(directory):
    folders = [dI for dI in os.listdir(directory) if os.path.isdir(os.path.join(directory,dI))]
    return folders

def list_hdf(directory):
    # files = [f for f in listdir(directory) if (isfile(join(directory, f))) & (f.endswith('.hdf') | f.endswith('.tif'))]
    files = [f for f in listdir(directory) if (isfile(join(directory, f))) & (f.endswith('.tif'))]
    return files

def main(folder):
    """
    

    Parameters
    ----------
    folder : str
        carpeta donde se guardan las imágenes MODIS.

    Returns
    -------
    None.

    """
# año inicial 2021
# año final: cualquiera sea el actual

    folder = os.path.abspath(os.path.join(folder,'Nieve'))
    
    year_f = date.today().year
        
    # obtener carpetas de años de imágenes MODIS
    
    for year in range(2021,year_f+1):
        # chequear si existe la carpeta de imágenes MODIS del año
        dir_out = os.path.join(folder,str(year))
        if str(year) not in list_folders(folder):
            os.mkdir(dir_out)
        
        # chequear los archivos MODIS
        onlyfiles = list_hdf(os.path.join(dir_out,'clip'))
        if len(onlyfiles):
            lastday = onlyfiles[-1].split('.')[1][-3:]
        else:
            lastday = 1
        
        # chequear si el año ya se bajó
        if calendar.isleap(year):
            if lastday == 366:
                continue
        elif lastday == 365:
            continue
        
        date_i = datetime.datetime(year, 1, 1) + datetime.timedelta(int(lastday) - 1)
        date_i = str(date_i.year)+'-'+str(date_i.month)+'-'+str(date_i.day)
        
        if year == year_f:
            date_f = date.today()
            date_f = str(date_f.year)+'-'+str(date_f.month)+'-'+str(date_f.day)
            download_MODIS.main(date_i, date_f, dir_out)
        else:
            date_f = datetime.datetime(year, 12, 31)
            date_f = str(date_f.year)+'-'+str(date_f.month)+'-'+str(date_f.day)
            download_MODIS.main(date_i, date_f, dir_out)

    return list(range(2021, year_f+1))
        
if __name__ == '__main__':
    main('.')
    