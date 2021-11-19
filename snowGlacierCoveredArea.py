# -*- coding: utf-8 -*-
"""
Created on Thu May 20 13:57:06 2021

@author: Carlos
"""

# ================================
#          librerias
# ================================
import matplotlib.pyplot as plt
import rasterio
import numpy as np
import pandas as pd
import xarray as xr
from scipy import interpolate
import rasterio
import rioxarray
import geopandas
from rasterio.features import shapes
from osgeo import gdal
import os
from osgeo import ogr
import datetime
import dask_geopandas

# ================================
#          funciones
# ================================

def findOffset(path_elev_463, path_modis):
    """
    

    Parameters
    ----------
    path_elev_463 : string
        ruta de las bandas de elevación resampleadas cada 500m.
    path_modis : string
        ruta de la imagen MODIS que se debe corregir.

    Returns
    -------
    None.

    """

    # realizar correlación 2d con fft entre las imágenes para obtener 
    # el desplazamiento de MODIS respecto a la cuenca
    
    import numpy as np
    from PIL import Image
    
    img1 = path_elev_463.data[0]
    img1[:,-1] = img1[:,-2] 
    img2 = np.asarray(Image.open(path_modis))
        
    from scipy import signal
    corr = signal.correlate2d(img1, img1, mode='same')
    y, x = np.unravel_index(np.argmax(corr), corr.shape)
    
    corr2 = signal.correlate2d(img1, img2, mode='same')
    y2, x2 = np.unravel_index(np.argmin(corr2), corr2.shape)
    
    return (x-x2,y-y2)


def modis_pre(i,year,ruta_modis,lista_modis):
    """
    

    Parameters
    ----------
    i : int
        día.
    year : int
        AÑO.
    ruta_modis : string
        ruta de la imagen MODIS.
    lista_modis : list
        lista de rutas.

    Returns
    -------
    modis_prev : xarray
        modis completada con el día anterior.

    """
    
    if i <= 0:
        # cargar la MODIS previa
        modis_prev =  xr.open_rasterio(os.path.join(ruta_modis,lista_modis[0]))
    else:
        # cargar la MODIS previa
        modis_prev =  xr.open_rasterio(os.path.join(ruta_modis,lista_modis[i-1]))
    return modis_prev
    
def modis_post(i,year,ruta_modis,lista_modis):
    """
    
    Parameters
    ----------
    i : int
        contador de imagen MODIS.
    year : int
        año.
    ruta_modis : str
        ruta de la carpeta donde se ubican las imágenes MODIS.
    lista_modis : list
        lista de rutas de imágenes MODIS.

    Returns
    -------
    modis_next : xarray
        xarray de raster de la imagen MODIS.

    """
     # MODIS del día siguiente
    if (i == len(lista_modis)-1) & (year >= 2021):
        modis_next =  xr.open_rasterio(os.path.join(ruta_modis,lista_modis[-1]))
    elif (i >= len(lista_modis)-1) & (year < 2021):
        # MODIS del día siguiente
        ruta_modis_next = ruta_modis.replace(str(year),str(year+1))
        lista_modis_next = os.listdir(ruta_modis_next)
        modis_next =  xr.open_rasterio(os.path.join(ruta_modis_next,lista_modis_next[0]))
    else:
        # MODIS del día siguiente
        modis_next =  xr.open_rasterio(os.path.join(ruta_modis,lista_modis[i+1]))
    return modis_next
    

def vtorast(vector_in):
    """
    

    Parameters
    ----------
    rast_in : str
        ruta del vector a transformar.
    dir_out : str
        directorio de salida del raster.

    Returns
    -------
    None.

    """
    
    input_shp = ogr.Open(vector_in)
    shp_layer = input_shp.GetLayer()
    
    pixel_size = 450
    xmin, xmax, ymin, ymax = shp_layer.GetExtent()
    
    ds = gdal.Rasterize(vector_in.replace('.shp','')+str('_raster.tif'), vector_in, xRes=pixel_size, yRes=pixel_size, 
                        attribute='fid', outputBounds=[xmin, ymin, xmax, ymax], 
                        outputType=gdal.GDT_Byte)
    
    ds = None
    
        
    elev_bands = xr.open_rasterio(vector_in.replace('.shp','')+'_raster.tif')
    elev_bands = elev_bands.astype(float)
    elev_bands.data[elev_bands.data == 0] = np.nan      
    elev_bands.rio.to_raster(vector_in.replace('.shp','')+'_raster_clip.tif', nodata = -99999)
    
    
# ===================================================================
def main(root_MODIS, yeari = datetime.date.today().year, yearf = datetime.date.today().year+1):
    """
    

    Parameters
    ----------
    ruta_OD : str
        ruta del directorio raíz de trabajo.
    subcuenca_modelo : str
        Nombre de la carpeta de la cuenca respectiva.
    ruta_eb_shp : str
        ruta del shapefile de bandas de elevación de la cuenca.
    ruta_gl : str
        ruta del shape de glaciares.
    ruta_elevaciones : str
        ruta del ráster de bandas de elevaciones.
    root_MODIS : str
        ruta de la carpeta donde se ubican las imágenes MODIS procesadas.

    Returns
    -------
    csvs de coberturas nivales y glaciares por banda de elevación.

    """
    
    # rutas
    ruta_eb_shp =  os.path.join(root_MODIS,'Shapes','bandas.shp')
    ruta_gl = os.path.join(root_MODIS,'Shapes','glaciares.shp')
    root_MODIS = os.path.abspath(os.path.join(root_MODIS,'Nieve'))
    
    flag = 1

    #%%    Años
    for year in range(yeari,yearf):
        # año y dias
        if year%4 == 0:
            days = 366
        else:
            days = 365
        

        ############################################################    
        #                leer shape glaciares
        ############################################################

        gdf_glaciar = geopandas.read_file(ruta_gl)
    
        ############################################################
        #             rutas de MODIS por cuenca
        ############################################################
    
        ruta_MODIS = os.path.join(root_MODIS,str(year),'clip')
         
        # cargar bandas de elevación
        shp_eb = geopandas.read_file(ruta_eb_shp)
        
        # convertirlo a raster
        
        vtorast(ruta_eb_shp)
        
        # leer bandas de elevacion                
        elev_xr = xr.open_rasterio(ruta_eb_shp.replace('.shp','')+'_raster_clip.tif')
        elev_xr.data[elev_xr.data == -99999] = 255
        
        # leer las bandas de elevación en raster
        elev_bands = xr.open_rasterio(ruta_eb_shp.replace('.shp','')+'_raster_clip.tif')
        elev_bands.data[elev_bands.data == 255] = 0
        bandas = int(np.nanmax(elev_bands.data))
    
        # listar los archivos de las imágenes MODIS
        lista_modis = os.listdir(ruta_MODIS)
        # filtrar los archivos temporales
        lista_modis = [x for x in lista_modis if x.endswith('.tif')]
        # ordenar la lista
        lista_modis = sorted(lista_modis)
        
        # resamplear la cuenca a la misma resolución de las MODIS
        modis_xr = xr.open_rasterio(os.path.join(ruta_MODIS,lista_modis[0]))
        elev_xr_rs = elev_xr.interp(x = modis_xr.x, y = modis_xr.y)
        
        # calcular el corrimiento
        (x, y) = findOffset(elev_xr_rs, os.path.join(ruta_MODIS,lista_modis[0]))
        # print((x, y))
    
        # corregir el desfase de las MODIS, esto se hace una sola vez
        if ((flag == 0) & (x != 0 | y != 0)):
            # revisar el corrimiento de las MODIS respecto a la cuenca
            print('Status: Aligning image data!')
        
            dx = 463.31271652836585
            dy = 463.31271652836585
            gdal.AllRegister()
            
            for file in lista_modis:
                rast_src = gdal.Open(os.path.join(ruta_MODIS,file), 1)
                gt = rast_src.GetGeoTransform()
                gtl = list(gt)
                
                gtl[0] += dx*x
                gtl[3] += dy*y
                rast_src.SetGeoTransform(tuple(gtl))
                rast_src = None
                
            flag += 1
        
        # crear df de dias y covertura nival
        snow_cover = pd.DataFrame([], index = list(range(0,days)), columns = list(range(bandas)))
        
        # crear df de dias y covertura glaciar
        glacial_cover = pd.DataFrame([], index = list(range(0,days)), columns = list(range(bandas)))
    
        # ===================================================
        #    Filtrado de nubes y corrección de imágenes
        # ===================================================
                      
        # crear la mascara de la MODIS en la cuenca
        modis_raster = xr.open_rasterio(os.path.join(ruta_MODIS,lista_modis[0]))
    
        # calcular áreas de cada celda sobre la cuenca del raster de MODIS
        # esto se debe hacer para cada banda de elevacion
        # copia de valores unicos de la MODIS para convertirlo a shape
        
        modis_raster = modis_raster.astype(float)
        
        if 'gpd_polygonized_raster' not in locals():
            size_modis = modis_raster.data[modis_raster.data != 255].size
            modis_unique = modis_raster.copy()
            uarray = np.random.choice(np.arange(0, size_modis*3), replace=False, size=(modis_unique.data.shape[1], modis_unique.data.shape[2]))
            uarray = uarray.astype(float)
            modis_unique.data[0,:,:] = uarray
            
            # convertir raster a shape
            results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) 
            in enumerate(
                shapes(modis_unique.astype(np.int32).data, mask=None, transform=modis_unique.transform)))
            geoms = list(results)
            gpd_polygonized_raster = geopandas.GeoDataFrame.from_features(geoms)
            gpd_polygonized_raster = gpd_polygonized_raster.set_crs(epsg = 32719)
            
            for banda in snow_cover.columns:
                
                # clip y calcular el área dentro de cada banda de elevacion
                shp_banda = geopandas.GeoDataFrame(shp_eb.iloc[banda])
                shp_banda = geopandas.GeoDataFrame(geometry = shp_banda.loc['geometry'])
                shp_banda = shp_banda.set_crs(epsg = 32719)
                
                # clip de las areas por banda de elevación usando Dask
                # create data
                ddf = dask_geopandas.from_geopandas(gpd_polygonized_raster, npartitions=4)
                
                # Esta es la máscara para clipear
                mask = shp_banda
                
                # Create more localized spatial partitions
                ddf = ddf.reset_index().persist()
                ddf.calculate_spatial_partitions()
                
                # Smarter version (~1.37s on my machine)
                new_spatial_partitions = geopandas.clip(ddf.spatial_partitions.to_frame('geometry'), mask)
                intersecting_partitions = np.asarray(new_spatial_partitions.index)
        
                name = 'clip-test'
                dsk = {(name, i): (geopandas.clip, (ddf._name, l), mask) for i, l in enumerate(intersecting_partitions)}
                divisions = [None] * (len(dsk) + 1)
                from dask.highlevelgraph import HighLevelGraph
                graph = HighLevelGraph.from_collections(name, dsk, dependencies=[ddf])
                result = dask_geopandas.core.GeoDataFrame(graph, name, ddf._meta, tuple(divisions))
                result.spatial_partitions = new_spatial_partitions
                
                gpd_polygonized_raster_c = result.compute()
                gpd_polygonized_raster_c.index = gpd_polygonized_raster_c['index']
                
                # clip área glaciar
                gpd_polygonized_raster_c_glaciar = geopandas.clip(gpd_polygonized_raster_c, gdf_glaciar)
                                                                      
                # inicializar áreas nivales dentro de la banda de elevación
                gpd_polygonized_raster["area_"+str(banda)] = 0
                # asignar áreas nivales dentro de la banda de elevación al raster de modis
                idx = gpd_polygonized_raster_c.index
                gpd_polygonized_raster.loc[idx,"area_"+str(banda)] = gpd_polygonized_raster_c['geometry'].area.values
                
                # inicializar áreas glaciares dentro de la banda de elevación
                gpd_polygonized_raster["areagl_"+str(banda)] = 0
                # asignar áreas glaciares dentro de la banda de elevación al raster de modis
                idx_gl = gpd_polygonized_raster_c_glaciar.index
                gpd_polygonized_raster.loc[idx_gl,"areagl_"+str(banda)] = gpd_polygonized_raster_c_glaciar['geometry'].area.values

        # procesar todos los días
        
        for m, modis in enumerate(lista_modis):

            # dia juliano
            dia = int(modis.split('.')[1][-3:])
                    
            # MODIS actual
            modis_current = xr.open_rasterio(os.path.join(ruta_MODIS,lista_modis[m]))
                    
            # MODIS del día siguiente
            modis_next = modis_post(m,year,ruta_MODIS,lista_modis)
            
            # # datos que no son nieve
            mask = np.isin(modis_next.data, [211,237,239])
            modis_next.data[mask] = 0   
        
            # reemplazar las nubes por nieve si existe nieve el día siguiente,
            # dado que y ya nevó el día anterior
            mask = (((modis_next.data <= 100) & (modis_next.data >= 0)) & ((modis_current.data == 250) | (modis_current.data == 201)))
            modis_current.data[mask] = modis_next.data[mask]
            
            # MODIS dia anterior
            modis_prev = modis_pre(m,year,ruta_MODIS,lista_modis)
            
            # datos que no son nieve
            mask = np.isin(modis_prev.data, [211,237,239])
            modis_prev.data[mask] = 0   
            
            # reemplazar las nubes (250) por nieve si existe nieve el día anterior
            mask = (((modis_prev.data <= 100) & (modis_prev.data >= 0)) & ((modis_current.data == 250) | (modis_current.data == 201)))
            modis_current.data[mask] = modis_prev.data[mask]
                    
            # datos vacíos y nubes que quedaron
            modis_current.data = modis_current.astype(float)
            mask = np.isin(modis_current.data, [200,201,254,250])
            modis_current.data[mask] = np.nan
            
            # datos que no son nieve
            mask = np.isin(modis_current.data, [211,237,239])
            modis_current.data[mask] = 0
            
            # datos afuera de la cuenca    
            modis_current.data[modis_current.data == 255.] = np.nan
                        
            # interpolar datos faltantes de la NASA
            #mask invalid values
            array = np.ma.masked_invalid(modis_current.data[0][:,:])
            x = np.arange(0, modis_current.data.shape[2])
            y = np.arange(0, modis_current.data.shape[1])
            xx, yy = np.meshgrid(x, y)
            #get only the valid values
            x1 = xx[~array.mask]
            y1 = yy[~array.mask]
            newarr = array[~array.mask]
            
            # loop recursivo para reconstruir varios días nublados considerando los datos desde 2000 y hasta 2021
            # Buscar hasta 1 semana de acuerd con con CNR (2015)
            if (year > 2000) & ((year < 2021) & (m < len(lista_modis)-7)):
                k = 1
                while ((len(newarr) <= size_modis) & (k < 6)):
                      # MODIS del día siguiente, parto por siguiente porque cuando se pierde la data es durante 
                      # las tormentas y días nublados
                    modis_next = modis_post(m+1+k,year,ruta_MODIS,lista_modis)
                    
                    # datos que no son nieve
                    mask = np.isin(modis_next.data, [211,237,239])
                    modis_next.data[mask] = 0   
                
                    # reemplazar las nubes por nieve si existe nieve el día siguiente,
                    # dado que y ya nevó el día anterior
                    mask = (((modis_next.data <= 100) & (modis_next.data >= 0)) & (np.isnan(modis_current.data)))
                    modis_current.data[mask] = modis_next.data[mask]
                    
                      # MODIS dia anterior
                    modis_prev = modis_pre(m-1-k,year,ruta_MODIS,lista_modis)
                    
                    # datos que no son nieve
                    mask = np.isin(modis_prev.data, [211,237,239])
                    modis_prev.data[mask] = 0            
                                            
                    # reemplazar las nubes (250) por nieve si existe nieve el día anterior
                    mask = (((modis_prev.data <= 100) & (modis_prev.data >= 0)) & (np.isnan(modis_current.data)))
                    modis_current.data[mask] = modis_prev.data[mask]
                            
                    # datos que no son nieve
                    mask = np.isin(modis_current.data, [211,237,239])
                    modis_current.data[mask] = 0
                                
                    # contar datos faltantes de la MODIS
                    #mask invalid values
                    array = np.ma.masked_invalid(modis_current.data[0][:,:])
                    x = np.arange(0, modis_current.data.shape[2])
                    y = np.arange(0, modis_current.data.shape[1])
                    xx, yy = np.meshgrid(x, y)
                    #get only the valid values
                    x1 = xx[~array.mask]
                    y1 = yy[~array.mask]
                    newarr = array[~array.mask]
                    k += 1
            else:
                            # loop recursivo para reconstruir varios días nublados
                k = 1
                while ((len(newarr) <= size_modis) & (k < 8)):
                      # MODIS del día siguiente, parto por siguiente porque cuando se pierde la data es durante 
                      # las tormentas y días nublados              
                    
                    # MODIS dia anterior
                    modis_prev = modis_pre(m-1-k,year,ruta_MODIS,lista_modis)
                    
                    # datos que no son nieve
                    mask = np.isin(modis_prev.data, [211,237,239])
                    modis_prev.data[mask] = 0            
                                            
                    # reemplazar las nubes (250) por nieve si existe nieve el día anterior
                    mask = (((modis_prev.data <= 100) & (modis_prev.data >= 0)) & (np.isnan(modis_current.data)))
                    modis_current.data[mask] = modis_prev.data[mask]
                            
                    # datos que no son nieve
                    mask = np.isin(modis_current.data, [211,237,239])
                    modis_current.data[mask] = 0
                                
                    # contar datos faltantes de la MODIS
                    #mask invalid values
                    array = np.ma.masked_invalid(modis_current.data[0][:,:])
                    x = np.arange(0, modis_current.data.shape[2])
                    y = np.arange(0, modis_current.data.shape[1])
                    xx, yy = np.meshgrid(x, y)
                    #get only the valid values
                    x1 = xx[~array.mask]
                    y1 = yy[~array.mask]
                    newarr = array[~array.mask]
                    k += 1
                
                    
            if len(newarr) < size_modis*.7:
                continue
                
            # interpolar datos faltantes       
            GD = interpolate.griddata((x1, y1), newarr.ravel(),
                                      (xx, yy),
                                      method='linear')
            modis_current.data = [GD]
            
            # pasar a fraccion cubierta nival SCF Salomonson and Appel 2004
            mask = (modis_current.data > 0) & (modis_current.data<=100)
            modis_current.data[mask] = 0.06+1.21*modis_current.data[mask]
            
            for j in range(len(snow_cover.columns)):
                # ponderar la cobertura nival por las areas 
                modis_current_banda = modis_current.copy()
                modis_current_banda.data[0] = modis_current_banda.data[0]*gpd_polygonized_raster.copy()["area_"+str(j)].values.reshape(modis_current_banda.data.shape[1],
                                                                                                                   modis_current_banda.data.shape[2])/100
                modis_current_banda.data[0][np.isnan(modis_current_banda.data[0])] = 0
                snow_cover.loc[dia-1,j] = np.sum(modis_current_banda.data[0])/shp_eb.geometry.area[j]
                
                # ponderar la cobertura glaciar por las areas 
                modis_current_banda_glaciar = modis_current.copy()
                modis_current_banda_glaciar.data[0] = modis_current_banda_glaciar.data[0]*gpd_polygonized_raster.copy()["areagl_"+str(j)].values.reshape(modis_current_banda.data.shape[1],
                                                                                                                                                         modis_current_banda.data.shape[2])/100
                # escribir cada banda de elevacion
                modis_current_banda_glaciar.data[0][np.isnan(modis_current_banda_glaciar.data[0])] = 0
                glacial_cover.loc[dia-1,j] = np.sum(modis_current_banda_glaciar.data[0])/np.sum(gpd_polygonized_raster.copy()["areagl_"+str(j)].values)
                    
        glacial_cover.fillna(0, inplace = True)
        snow_cover[snow_cover.columns] = snow_cover[snow_cover.columns].fillna(snow_cover[snow_cover.columns].rolling(60,center=False,min_periods=1).mean())  
        glacial_cover[glacial_cover.columns] = glacial_cover[glacial_cover.columns].fillna(glacial_cover[glacial_cover.columns].rolling(30,center=False,min_periods=1).mean())  
    
        indice = pd.date_range(str(year)+'-01-01',str(year)+'-12-31',freq = '1d')
        snow_cover.index = indice
        glacial_cover.index = indice
    
        #% plots    
        # plt.close("all")
        # fig , ax = plt.subplots(5,5)
        # ax = ax.reshape(-1)
        
        # for i,axis in enumerate(snow_cover.columns):
        #     snow_cover.iloc[:,i].plot(ax = ax[i])
        #     ax[i].set_ylim(bottom = 0, top = 1)    
        #     ax[i].set_ylabel('Cob. nival') 
        #     for tick in ax[i].xaxis.get_major_ticks():
        #         tick.label.set_fontsize(8)
        # for i in range(19,25):
        #     fig.delaxes(ax[i])
            
        # # plot glacier
        # fig , ax = plt.subplots(5,5)
        # ax = ax.reshape(-1)
        
        # for i,axis in enumerate(snow_cover.columns):
        #     glacial_cover.iloc[:,i].plot(ax = ax[i])
        #     ax[i].set_ylim(bottom = 0, top = 1)    
        #     ax[i].set_ylabel('Cob. nival') 
        #     for tick in ax[i].xaxis.get_major_ticks():
        #         tick.label.set_fontsize(8)
        # for i in range(19,25):
        #     fig.delaxes(ax[i])
        
        snow_cover.iloc[dia-1:,:] = np.nan
        glacial_cover.iloc[dia-1:,:] = np.nan
    
        #%% guardar el df de coberturas nivales y glaciares
       
        snow_cover.to_csv(os.path.join(root_MODIS,r'DailySnowCover'+str(year)+'.csv'))
        glacial_cover.to_csv(os.path.join(root_MODIS,r'DailyGlacialCover'+str(year)+'.csv'))
