# -*- coding: utf-8 -*-
"""
Created on Tue May 18 19:01:23 2021

@author: Carlos
"""

# librerias
import rasterio
import rasterio.mask
import fiona
import os
import datetime

def Process_MODIS(dir_in, dir_out, shp, yr):
    """
    

    Parameters
    ----------
    dir_in : string
        directorio de entrada.
    dir_out : string
        directorio de salida.
    shp : string
        ruta del shape.
    yr : int
        año de las MODIS.

    Returns
    -------
    None.

    """
    
    # setear directorios de entrada y de salida
    dir_in = os.path.join(dir_in,str(yr),'prm','reproj')
    dir_out = os.path.join(dir_out,str(yr),'clip')
    
    # cargar shape de la cuenca
    shp = fiona.open(shp)
    shapes = [feature["geometry"] for feature in shp]
    
    # crear directorio de salida
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)   
    
    # leet las imágenes MODIS
    for filename in os.listdir(dir_in):
        # if (filename.endswith(".tif")) & ('h12v12' in filename): 
        if filename.endswith(".tif"): 
            raster = rasterio.open(dir_in+'\\'+filename,
                                     masked=True)
            
            # clip
            out_image, out_transform = rasterio.mask.mask(raster, shapes, crop= True, all_touched = True)
            out_meta = raster.meta
            out_meta.update({"driver": "GTiff",
                             "height": out_image.shape[1],
                             "width": out_image.shape[2],
                             "transform": out_transform})
            # save
            with rasterio.open(dir_out+'\\'+filename.replace('.tif','')+'_clp.tif', "w", **out_meta) as dest:
                dest.write(out_image)
                
    return None

def main(dir_in,  yeari = datetime.date.today().year, yearf = datetime.date.today().year+1):

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

    shp = os.path.abspath(os.path.join(dir_in,'Shapes','bandas.shp'))
    dir_in = os.path.abspath(os.path.join(dir_in,'Nieve'))
    dir_out = dir_in
    
    for yr in range(yeari,yearf):
        Process_MODIS(dir_in, dir_out, shp, str(yr))
    return None
 
if __name__ == '__main__':
    main()
    