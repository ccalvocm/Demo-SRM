#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 13:16:23 2021

@author: faarrosp
"""

import ee
import geemap
import os
import geopandas as gpd
import pandas as pd
# from shapely.geometry import Point
# from shapely.ops import transform
# import pyproj

dic_subcuencas = {'01_RMELA': 'Rio Mapocho en Los Almendros',
                  '02_RMEEM': 'Rio Maipo en El Manzano',
                  '01_RCEPTDC': 'Rio Cachapoal en Puente Termas de Cauquenes',
                  '02_RCEHLN': 'Rio Claro en Hacienda Las Nieves',
                  '03_RTBLB': 'Rio Tinguiririca bajo Los Briones'}

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
    
    # Set visualization parameters.
    # vis_params = {
    #   'min': 0,
    #   'max': 4000,
    #   'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}
    
    # Add Earth Eninge layers to Map
    # Map.addLayer(dem, vis_params, 'SRTM DEM', True, 0.5)
    # Map.addLayer(landcover, {}, 'Land cover')
    # Map.addLayer(landsat7, {'bands': ['B4', 'B3', 'B2'], 'min': 20, 'max': 200, 'gamma':1.5}, 'Landsat 7')
    # Map.addLayer(states, {}, "US States")
    
    
    # if not os.path.exists(download_dir):
    #     os.makedirs(download_dir)
    html_file = os.path.join(os.getcwd(), layer_code + '.html')
    Map.to_html(outfile=html_file, title='Mapa', width='100%', height='880px')
    
    
def create_4326_shapefile(filepath):
    gdf = gpd.read_file(filepath)
    gdf = gdf.to_crs('EPSG:4326')
    gdf.to_file(filepath[:-4] + '_4326.shp')
    
if __name__ == '__main__':
    
    subcuenca = os.path.join(*['02_Rapel', '03_RTBLB'])
    
    shp_file_path = os.path.join(subcuenca,'Shapes', 'cuenca.shp')
    create_4326_shapefile(shp_file_path)
    
    shp_file_path2 = os.path.join(subcuenca,'Shapes', 'cuenca_4326.shp')
    export_html_map(shp_file_path2)
    
    