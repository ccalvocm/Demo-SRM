#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 13:16:23 2021

@author: faarrosp
"""

import ee
service_account = 'srmearthenginelogin@srmlogin.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, '.\\interfaz_descarga_GEE\\srmlogin-ec74c9d43705.json')
ee.Initialize(credentials)
import geemap
import os
import geopandas as gpd
import pandas as pd


dic_subcuencas = {'01_RMELA': 'Rio Mapocho en Los Almendros',
                  '02_RMEEM': 'Rio Maipo en El Manzano',
                  '01_RCEPTDC': 'Rio Cachapoal en Puente Termas de Cauquenes',
                  '02_RCEHLN': 'Rio Claro en Hacienda Las Nieves',
                  '03_RTBLB': 'Rio Tinguiririca bajo Los Briones',
                  '01_RTDJCC': 'Rio Teno despues de junta con Claro',
                  '02_RCEJCP': 'Rio Colorado en junta con Palos',
                  '03_RPEJCC': 'Rio Palos en junta con Colorado',
                  '01_RMEA': 'Rio Maule en Armerillo'}
dic_cuencas = {'01_Maipo': ['01_RMELA', '02_RMEEM'],
               '02_Rapel': ['01_RCEPTDC', '02_RCEHLN', '03_RTBLB'],
               '03_Mataquito': ['01_RTDJCC', '02_RCEJCP', '03_RPEJCC'],
               '04_Maule': ['01_RMEA']}

def export_html_map(shp_file_path):


    Map = geemap.Map(toolbar_ctrl=True, layer_ctrl=True)
    
    
    gdf = gpd.read_file(shp_file_path)
    
    gdf_aux = gdf.to_crs('EPSG:32719')
    
    lon = float(round(gdf_aux.geometry.centroid.x.values[0],3))
    lat = float(round(gdf_aux.geometry.centroid.y.values[0],3))
    
    df = pd.DataFrame({'x': [lon], 'y': [lat]})
    gdf_new = gpd.GeoDataFrame(df,
                               geometry = gpd.points_from_xy(df['x'],
                                                                   df['y'],
                                                                   crs='EPSG:32719'))
    
    
    gdf_new = gdf_new.to_crs('EPSG:4326')  
    
    print(gdf_new['geometry'].x.values[0],
          gdf_new['geometry'].y.values[0])
    
    lon = float(round(gdf_new['geometry'].x.values[0],3))
    lat = float(round(gdf_new['geometry'].y.values[0],3))
    
    print(lon,lat)
    
    zoom = 8
    Map.setCenter(lon, lat, zoom)
    layer_code = shp_file_path.split('/')[-3]
    layer_name = dic_subcuencas[layer_code]
    ee_object = geemap.shp_to_ee(shp_file_path)
    Map.addLayer(ee_object, {}, layer_name)    
    
    html_file = os.path.join(os.getcwd(),'basemaps', layer_code + '.html')
    Map.to_html(outfile=html_file, title='Mapa', width='100%', height='880px')
    
    
def create_4326_shapefile(filepath):
    gdf = gpd.read_file(filepath)
    gdf = gdf.to_crs('EPSG:4326')
    gdf.to_file(filepath[:-4] + '_4326.shp')
    
def write_centroids():
    with open('centroides.csv', 'w') as file:
        for key in dic_cuencas.keys():
            for cuenca in dic_cuencas[key]:
                subcuenca = os.path.join(*[key,cuenca])
                shp_file_path = os.path.join(subcuenca,'Shapes', 'cuenca.shp')
                gdf = gpd.read_file(shp_file_path)
        
                gdf_aux = gdf.to_crs('EPSG:32719')
                lon = float(round(gdf_aux.geometry.centroid.x.values[0],3))
                lat = float(round(gdf_aux.geometry.centroid.y.values[0],3))
                
                df = pd.DataFrame({'x': [lon], 'y': [lat]})
                gdf_new = \
                    gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['x'],
                                                                       df['y'],
                                                                       crs='EPSG:32719'))        
                gdf_new = gdf_new.to_crs('EPSG:4326')
                lon = str(float(round(gdf_new['geometry'].x.values[0],3)))
                lat = str(float(round(gdf_new['geometry'].y.values[0],3)))
                
                file.write(','.join([subcuenca,lon,lat])+'\n')
        
def renew_html_maps():
    df_centroides = pd.read_csv('centroides.csv',header=None, index_col=1)
    for key in dic_cuencas.keys():
        for cuenca in dic_cuencas[key]:
            ruta_shape = os.path.join(*[key,cuenca,'Shapes','cuenca_4326.shp'])
            loc = cuenca
            lon = float(df_centroides.loc[loc,2])
            lat = float(df_centroides.loc[loc,3])
            Map = geemap.Map(toolbar_ctrl=True, layer_ctrl=True)
            Map.add_basemap('OpenTopoMap')
            zoom = 8
            Map.setCenter(lon, lat, zoom)
            ee_object = geemap.shp_to_ee(ruta_shape)
            layer_name = dic_subcuencas[cuenca]
            Map.addLayer(ee_object, name = layer_name,
                         opacity=0.8)
            html_file = os.path.join(os.getcwd(), 'basemaps', cuenca + '.html')
            Map.to_html(outfile=html_file, title='Mapa', width='100%',
                        height='880px')
            
    
if __name__ == '__main__':
    
    renew_html_maps()
    
    