#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:17:00 2021

@author: faarrosp
"""
# MODULO multigeometry

from functools import singledispatch
from itertools import chain
from typing import (List, 
                    Tuple,
                    TypeVar)

from shapely.geometry import (GeometryCollection,
                              LinearRing,
                              LineString,
                              Point,
                              Polygon)
from shapely.geometry.base import (BaseGeometry,
                                   BaseMultipartGeometry)


import numpy as np
import shapely as sh
import datetime
import ee
import os
service_account = 'srmearthenginelogin@srmlogin.iam.gserviceaccount.com'
folder_json = os.path.join('.','interfaz_descarga_GEE','srmlogin-175106b08655.json')
credentials = ee.ServiceAccountCredentials(service_account, folder_json)
ee.Initialize(credentials)

def get_dataset_dates(dataset_str):
    ee.Initialize(credentials)
    collection = ee.ImageCollection(dataset_str)
    date_range = collection.reduceColumns(ee.Reducer.minMax(),
                                          ['system:time_start'])
    jsondate1 = ee.Date(date_range.get('min'))
    jsondate2 = ee.Date(date_range.get('max'))
    
    pydate1 = datetime.datetime.\
        utcfromtimestamp(jsondate1.getInfo()['value']/1000.0)
    pydate2 = datetime.datetime.\
        utcfromtimestamp(jsondate2.getInfo()['value']/1000.0)
    
    datestr1 = pydate1.strftime('%Y-%m-%d')
    datestr2 = pydate2.strftime('%Y-%m-%d')
    
    # print(datestr1,datestr2)
    return [datestr1,datestr2]
    

def getPolyCoords(geom, coord_type):
    """Returns the coordinates ('x|y') of edges/vertices of a Polygon/others"""

    # Parse the geometries and grab the coordinate
    geometry = geom
    #print(geometry.type)

    if geometry.type=='Polygon':
        if coord_type == 'x':
            # Get the x coordinates of the exterior
            # Interior is more complex: xxx.interiors[0].coords.xy[0]
            return list( geometry.exterior.coords.xy[0] )
        elif coord_type == 'y':
            # Get the y coordinates of the exterior
            return list( geometry.exterior.coords.xy[1] )

    if geometry.type in ['Point', 'LineString']:
        if coord_type == 'x':
            return list( geometry.xy[0] )
        elif coord_type == 'y':
            return list( geometry.xy[1] )

    if geometry.type=='MultiLineString':
        all_xy = []
        for ea in geometry:
            if coord_type == 'x':
                all_xy.append(list( ea.xy[0] ))
            elif coord_type == 'y':
                all_xy.append(list( ea.xy[1] ))
        return all_xy

    if geometry.type=='MultiPolygon':
        all_xy = []
        for ea in geometry:
            if coord_type == 'x':
                all_xy.append(list( ea.exterior.coords.xy[0] ))
            elif coord_type == 'y':
                all_xy.append(list( ea.exterior.coords.xy[1] ))
        return all_xy

    else:
        # Finally, return empty list for unknown geometries
        return []

Geometry = TypeVar('Geometry', bound=BaseGeometry)


@singledispatch
def to_coords(geometry: Geometry) -> List[Tuple[float, float]]:
    """Returns a list of unique vertices of a given geometry object."""
    raise NotImplementedError(f"Unsupported Geometry {type(geometry)}")


@to_coords.register
def _(geometry: Point):
    return [(geometry.x, geometry.y)]


@to_coords.register
def _(geometry: LineString):
    return list(geometry.coords)


@to_coords.register
def _(geometry: LinearRing):
    return list(geometry.coords[:-1])


@to_coords.register
def _(geometry: BaseMultipartGeometry):
    return list(set(chain.from_iterable(map(to_coords, geometry))))


@to_coords.register
def _(geometry: Polygon):
    return to_coords(GeometryCollection([geometry.exterior, *geometry.interiors]))

# MODULO GOOGLE EARTH ENGINE DOWNLOAD
    # diccionario de shapes de cuencas
    
import ee
import pandas as pd
import time
ee.Initialize(credentials)
import multigeometry
import json
    
dic_shp_bandas = {'Maipo': {'MLAL': 'MLAL_EB_250.shp',
                            'MEEM': 'Bandas_MEEM_250.shp'},
                  'Rapel': {'RCEHLN': 'EB_250_RCEHLN_DGA.shp',
                            'RCEPTDC': 'EB_250_RCEPTDC.shp',
                            'RTBLB': 'EB_250_RTBLB.shp'},
                  'Mataquito': {'RCJCP': 'EB_250_RCJP.shp',
                                'RPJCC': 'EB_250_RPJCC.shp',
                                'RTDJCC': 'EB_250_RTDJCC.shp'},
                  'Maule': {'RMEA': 'EB_250_RMEA.shp'}}

dic_shp_cuenca = {'Maipo': {'MLAL': 'MLAL_EB_250_Dissolved.shp',
                            'MEEM': 'Maipo en el Manzano Fixed geometries.shp'},
                  'Rapel': {'RCEHLN': 'cuenca_RCHLN_DGA.shp',
                            'RCEPTDC': 'EB_250_RCEPTDC_Dissolved.shp',
                            'RTBLB': 'cuenca_RTBLB.shp'},
                  'Mataquito': {'RCJCP': 'cuenca_RCJP_Dissolved.shp',
                                'RPJCC': 'cuenca_RPJCC.shp',
                                'RTDJCC': 'Cuenca_RTDJCC_Dissolved.shp'},
                  'Maule': {'RMEA': 'Cuenca_RMEA_Dissolved.shp'}}

    # diccionarios de datasets descargar

gee_names = {'GPM': "NASA/GPM_L3/IMERG_V06",
                 'PERSIANN': "NOAA/PERSIANN-CDR",
                 'ERA5dayP': "ECMWF/ERA5/DAILY",
                 'ERA5dayT': "ECMWF/ERA5/DAILY",
                 'ERA5hourT2m': 'ECMWF/ERA5_LAND/HOURLY',
                 'ERA5hourly_snow_density': 'ECMWF/ERA5_LAND/HOURLY',
                 'ERA5hourly_SWE': 'ECMWF/ERA5_LAND/HOURLY',
                 'CHIRPSday': "UCSB-CHG/CHIRPS/DAILY",
                 'FLDASdayT': "NASA/FLDAS/NOAH01/C/GL/M/V001",
                 'GLDAS21_ta': "NASA/GLDAS/V021/NOAH/G025/T3H",
                 'GLDAS21_pres': "NASA/GLDAS/V021/NOAH/G025/T3H",
                 'GLDAS21_hum': "NASA/GLDAS/V021/NOAH/G025/T3H",
                 'GLDAS21_SWE': "NASA/GLDAS/V021/NOAH/G025/T3H",
                 'GLDAS21_wsp': "NASA/GLDAS/V021/NOAH/G025/T3H",
                 'GLDAS21_ET': "NASA/GLDAS/V021/NOAH/G025/T3H",
                 'CFSR_T': "NOAA/CFSR",
                 'CFSR_T2m': "NOAA/CFSR",
                 'CFSV2_T2m': 'NOAA/CFSV2/FOR6H'}

img_path = './interfaz_descarga_GEE/thumbnails/'
dic_productos = {'GPM': {'name': 'Global Precipitation Measurement (GPM) v6',
                         'sigla': 'GPM',
                         'snippet': 'NASA/GPM_L3/IMERG_V06',
                         'dates': get_dataset_dates('NASA/GPM_L3/IMERG_V06'),
                         # 'dates': ['2000-06-01','2021-07-30'],
                         'scale': 0.1 * 110 * 1000,
                         'tres': '30-min',
                         'variables': {'pr': 'precipitationCal'},
                         'img_preview': img_path + 'GPM_IMERG_sample.png'},
                 'PERSIANN': {'name': 'Precipitation Estimation From Remotely Sensed Information Using Artificial Neural Networks-Climate Data Record',
                              'sigla': 'PERSIANN-CDR',
                              'snippet': 'NOAA/PERSIANN-CDR',
                              # 'dates': ['1983-01-01','2021-04-01'],
                              'dates': get_dataset_dates('NOAA/PERSIANN-CDR'),
                              'scale': 0.25 * 110 * 1000,
                              'tres': 'daily',
                              'variables': {'pr': 'precipitation'},
                              'img_preview': img_path + \
                                  'NOAA_PERSIANN-CDR_sample.png'},
                 'ERA5_daily': {'name': 'ERA5 Daily Aggregates - Latest Climate Reanalysis Produced by ECMWF / Copernicus Climate Change Service',
                                'sigla': 'ERA5',
                                'snippet': 'ECMWF/ERA5/DAILY',
                                # 'dates': ['1979-01-02', '2020-07-09'],
                                'dates': get_dataset_dates('ECMWF/ERA5/DAILY'),
                                'scale': 0.25 * 110 * 1000,
                                'tres': 'daily',
                                'variables': {'pr': 'total_precipitation',
                                              't2m': 'mean_2m_air_temperature',
                                              'pres': 'surface_pressure'},
                                'img_preview': img_path + \
                                    'ECMWF_ERA5_DAILY_sample.png'},
                 'ERA5_hourly': {'name': 'ERA5-Land Hourly - ECMWF Climate Reanalysis',
                                 'sigla': 'ERA5',
                                 'snippet': 'ECMWF/ERA5_LAND/HOURLY',
                                 # 'dates': ['1981-01-01', '2021-06-30'],
                                 'dates': get_dataset_dates('ECMWF/ERA5_LAND/HOURLY'),
                                 'scale': 0.1 * 110 * 1000,
                                 'tres': 'hourly',
                                 'variables': {'t2m': 'temperature_2m',
                                               'snow_density': 'snow_density',
                                               'swe': 'snow_depth_water_equivalent'},
                                 'img_preview': img_path + \
                                     'ERA5_LAND_HOURLY_sample.png'},
                 'CHIRPS': {'name': 'CHIRPS Daily: Climate Hazards Group InfraRed Precipitation With Station Data (Version 2.0 Final)',
                            'sigla': 'CHIRPS',
                            'snippet': 'UCSB-CHG/CHIRPS/DAILY',
                            # 'dates': ['1981-01-01', '2021-07-31'],
                            'dates': get_dataset_dates('UCSB-CHG/CHIRPS/DAILY'),
                            'scale': 0.05 * 110 * 1000,
                            'tres': 'daily',
                            'variables': {'pr': 'precipitation'},
                            'img_preview': img_path + \
                                'CHIRPS_sample.png'},
                 'GLDAS_2_1': {'name': 'GLDAS-2.1: Global Land Data Assimilation System',
                               'sigla': 'GLDAS 2.1',
                               'snippet': 'NASA/GLDAS/V021/NOAH/G025/T3H',
                               # 'dates': ['2000-01-01', '2021-08-06'],
                               'dates': get_dataset_dates('NASA/GLDAS/V021/NOAH/G025/T3H'),
                               'scale': 0.25 * 110 * 1000,
                               'tres': '3-hourly',
                               'variables': {'t2m': 'Tair_f_inst',
                                             'swe': 'SWE_inst',
                                             'ET': 'Evap_tavg',
                                             'pres': 'Psurf_f_inst',
                                             'hum_sp': 'Qair_f_inst',
                                             'wind_sp': 'Wind_f_inst'},
                               'img_preview': img_path + \
                                   'NASA_GLDAS_sample.png'},
                 'CFSV2': {'name': 'CFSV2: NCEP Climate Forecast System Version 2, 6-Hourly Products',
                           'sigla': 'CFSV',
                           'snippet': 'NOAA/CFSV2/FOR6H',
                           # 'dates': ['1979-01-01', '2021-09-06'],
                           'dates': get_dataset_dates('NOAA/CFSV2/FOR6H'),
                           'scale': 0.2 * 110 * 1000,
                           'tres': '6-hourly',
                           'variables': {'pres': 'Pressure_surface',
                                         't2m': 'Temperature_height_above_ground',
                                         'hum_sp': 'Specific_humidity_height_above_ground'},
                           'img_preview': img_path + \
                               'NOAA_CFSV2_FOR6H_sample.png'}}

class dataset:
    def __init__(self,dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
            
def dataset_description(dataset):
    str_nombre = dataset.name
    str_sigla = dataset.sigla
    str_dates = dataset.dates[0] + ' a ' + dataset.dates[1]
    str_scale = str(dataset.scale) + ' mts'
    
    dic_tres = {'30-min': 'Cada 30 minutos',
                'hourly': 'Cada 1 hora',
                '3-hourly': 'Cada 3 horas',
                '6-hourly': 'Cada 6 horas',
                'daily': 'Cada 1 dia'}
    str_tres = dic_tres[dataset.tres]
    str_variables = json.dumps(dataset.variables)
    str_variables = str_variables.replace(',', '\n')
    
    descripcion = '\n'.join(['Sigla: ' + str_sigla,
                             ' ',
                             'Nombre: ' + str_nombre,
                             ' ',
                             'Frecuencia: ' + str_tres,
                             ' ',
                             'Resolucion espacial: ' + str_scale,
                             ' ',
                             'Disponibilidad temporal: ' + str_dates,
                             ' ',
                             ])
    
    return descripcion



    
dates = {'GPM': ['2000-06-01','2021-07-30'],
         'PERSIANN': ['1983-01-01','2021-04-01'],
         'ERA5dayP': ['1979-01-02','2020-07-09'],
         'ERA5dayT': ['2000-01-01','2020-07-09'],
         'ERA5hourT2m': ['2000-01-01', '2000-06-30'],
         'ERA5hourly_snow_density': ['2000-01-01', '2021-05-30'],
         'ERA5hourly_SWE': ['2000-01-01', '2021-05-30'],
         'CHIRPSday': ['2000-01-01','2021-06-30'],
         'FLDASdayT': ['1982-01-01', '2021-06-01'],
         'GLDAS21_ta': ['2000-01-01', '2021-07-05'],
         'GLDAS21_pres': ['2000-01-01', '2021-07-05'],
         'GLDAS21_hum': ['2000-01-01', '2021-07-05'],
         'GLDAS21_SWE': ['2000-01-01', '2021-07-05'],
         'GLDAS21_wsp': ['2000-01-01', '2021-07-05'],
         'GLDAS21_ET': ['2000-01-01', '2021-07-05'],
         'CFSR_T': ['2000-01-01', '2021-07-05'],
         'CFSR_T2m': ['2006-01-01', '2011-12-31'],
         'CFSV2_T2m': ['2000-01-01', '2021-09-06']}

layers = {'GPM': 'precipitationCal',
          'PERSIANN': 'precipitation',
          'ERA5dayP': 'total_precipitation',
          'ERA5dayT': 'mean_2m_air_temperature',
          'ERA5hourT2m': 'temperature_2m',
          'ERA5hourly_snow_density': 'snow_density',
          'ERA5hourly_SWE': 'snow_depth_water_equivalent',
          'CHIRPSday': 'precipitation',
          'FLDASdayT': 'Tair_f_tavg',
          'GLDAS21_ta': 'Tair_f_inst',
          'GLDAS21_pres': 'Psurf_f_inst',
          'GLDAS21_hum': 'Qair_f_inst',
          'GLDAS21_SWE': 'SWE_inst',
          'GLDAS21_wsp': 'Wind_f_inst',
          'GLDAS21_ET': 'Evap_tavg',
          'CFSR_T': 'Temperature_surface',
          'CFSR_T2m': 'Temperature_at_2m_height_above_ground',
          'CFSV2_T2m': 'Temperature_height_above_ground'}


scales = {'GPM': 0.1 * 110 * 1000,
          'PERSIANN': 0.25 * 110 * 1000,
          'ERA5dayP': 0.25 * 110 * 1000,
          'ERA5dayT': 0.25 * 110 * 1000,
          'ERA5hourT2m': 0.1 * 110 * 1000,
          'ERA5hourly_snow_density': 0.1 * 110 * 1000,
          'ERA5hourly_SWE': 0.1 * 110 * 1000,
          'CHIRPSday': 0.05 * 110 * 1000,
          'FLDASdayT': 0.1 * 110 * 1000,
          'GLDAS21_ta': 0.25 * 110 * 1000,
          'GLDAS21_pres': 0.25 * 110 * 1000,
          'GLDAS21_hum': 0.25 * 110 * 1000,
          'GLDAS21_SWE': 0.25 * 110 * 1000,
          'GLDAS21_wsp': 0.25 * 110 * 1000,
          'GLDAS21_ET': 0.25 * 110 * 1000,
          'CFSR_T': 0.5 * 110 * 1000,
          'CFSR_T2m': 0.5 * 110 * 1000,
          'CFSV2_T2m': 0.2 * 110 * 1000}

def point_sample(lon,lat,dataset_str,date1,date2,buffer=500):
    ee.Initialize(credentials)
    point = ee.Geometry.Point([lon,lat]).buffer(2500)
    collection = ee.ImageCollection(gee_names[dataset_str]).filterBounds(point)
    collectionF = collection.select(layers[dataset_str]).filterDate(date1,date2)
    
    # define mapping function
    def point_mean(img):
        mean = img.reduceRegion(reducer=ee.Reducer.mean(),
                                geometry=point,
                                scale=scales[dataset_str]).get(layers[dataset_str])
        return img.set('date', img.date().format()).set('mean',mean)
    
    poi_reduced_imgs = collectionF.map(point_mean)
    t1 = time.time()
    dl = False
    dlon = round(lon,2)
    dlat = round(lat,2)
    
    while ~dl:
        try:
            print('Intentando descargar', dataset_str, 'punto', [dlon,dlat])
            nested_list = poi_reduced_imgs.reduceColumns(ee.Reducer.toList(2), ['date','mean']).values().get(0)
            df = pd.DataFrame(nested_list.getInfo(), columns=['date','mean'])
            t2 = time.time()
            print('Descarga OK', 'tiempo', round((t2-t1)/60,2), 'minutos')
            dl = True
            break
        except:
            print('Intento fallido')
            dl = False
            
    df.set_index('date',inplace=True)
    serie = df['mean']
    serie.index = pd.to_datetime(serie.index)
    serie.rename(dataset_str,inplace=True)
    Serie = serie
    if dataset_str == 'GPM':
        Serie = Serie * 0.5
        Serie = Serie.resample('D').sum()
    elif dataset_str == 'ERA5dayP':
        Serie = Serie * 1000
        
    elif dataset_str in ['ERA5dayT', 'FLDASdayT']:
        Serie = Serie - 273.15
        
    elif dataset_str == 'GLDAS21':
        Serie = Serie - 273.15
        Serie = Serie.resample('D').mean()
        
    elif dataset_str == 'GLDAS21_pres':
        Serie = Serie.resample('D').mean()
        
    elif dataset_str == 'GLDAS21_hum':
        Serie = Serie.resample('D').mean()
        
    elif dataset_str == 'GLDAS21_ET':
        Serie = Serie.resample('D').mean()
    
    elif dataset_str == 'ERA5hourT2m':
        Serie = Serie.resample('D').mean()
        Serie = Serie - 273.15
        
    elif dataset_str == 'CFSV2_T2m':
        Serie = Serie.resample('D').mean()
        Serie = Serie - 273.15
    
    return Serie


def polygon_sample(geometry,dataset_str,date1,date2):
    ee.Initialize(credentials)
    x = multigeometry.getPolyCoords(geometry, 'x')
    y = multigeometry.getPolyCoords(geometry, 'y')
    coords = np.dstack((x,y)).tolist()
    roi = ee.Geometry.Polygon(coords)
    bounds = roi.bounds()
    collection = ee.ImageCollection(gee_names[dataset_str]).filterBounds(bounds)
    collectionF = collection.select(layers[dataset_str]).filterDate(date1,date2)
    
    # define mapping function
    def point_mean(img):
        mean = img.reduceRegion(reducer=ee.Reducer.mean(),
                                geometry=roi,
                                scale=scales[dataset_str]).get(layers[dataset_str])
        return img.set('date', img.date().format()).set('mean',mean)
    
    poi_reduced_imgs = collectionF.map(point_mean)
    t1 = time.time()
    dl = False
    
    while ~dl:
        try:
            print('Intentando descargar', dataset_str)
            nested_list = poi_reduced_imgs.reduceColumns(ee.Reducer.toList(2), ['date','mean']).values().get(0)
            df = pd.DataFrame(nested_list.getInfo(), columns=['date','mean'])
            t2 = time.time()
            print('Descarga OK', 'tiempo', round((t2-t1)/60,2), 'minutos')
            dl = True
            break
        except:
            print('Intento fallido')
            dl = False
            
    df.set_index('date',inplace=True)
    serie = df['mean']
    serie.index = pd.to_datetime(serie.index)
    serie.rename(dataset_str,inplace=True)
    Serie = serie
    if dataset_str == 'GPM':
        Serie = Serie * 0.5
        Serie = Serie.resample('D').sum()
    elif dataset_str == 'ERA5dayP':
        Serie = Serie * 1000
        
    elif dataset_str in ['ERA5dayT', 'FLDASdayT']:
        Serie = Serie - 273.15
        
    elif dataset_str == 'GLDAS21_ta':
        Serie = Serie - 273.15
        Serie = Serie.resample('D').mean()
        
    elif dataset_str == 'GLDAS21_pres':
        Serie = Serie.resample('D').mean()
        
    elif dataset_str == 'GLDAS21_hum':
        Serie = Serie.resample('D').mean()
        
    elif dataset_str == 'GLDAS21_ET':
        Serie = Serie.resample('D').mean()
        
    elif dataset_str == 'ERA5hourT2m':
        Serie = Serie.resample('D').mean()
        Serie = Serie - 273.15
        
    elif dataset_str == 'CFSV2_T2m':
        Serie = Serie.resample('D').mean()
        Serie = Serie - 273.15
    
    return Serie

def polygon_sample2(geometry,connection, variable, date1,date2):
    # inicializar Google Earth Engine
    # ee.Initialize()
    
    # Definir las coordenadas del poligono
    x = multigeometry.getPolyCoords(geometry, 'x')
    y = multigeometry.getPolyCoords(geometry, 'y')
    coords = np.dstack((x,y)).tolist()
    roi = ee.Geometry.Polygon(coords)
    bounds = roi.bounds()
    
    dataset_name = connection.snippet
    # variable_name = connection.variables[variable]
    variable_name = variable
    scale_value = connection.scale
    frequency_value = connection.tres
    
    
    # Coleccion de Google Earth Engine
    collection = ee.ImageCollection(dataset_name).filterBounds(bounds)
    collectionF = collection.select(variable_name).filterDate(date1,date2)
    
    # define mapping function
    def point_mean(img):
        mean = img.reduceRegion(reducer=ee.Reducer.mean(),
                                geometry=roi,
                                # scale=scale_value,
                                bestEffort=True).get(variable_name)
        return img.set('date', img.date().format()).set('mean',mean)
    
    poi_reduced_imgs = collectionF.map(point_mean)
    t1 = time.time()
    dl = False
    
    while ~dl:
        try:
            print('Intentando descargar')
            nested_list = poi_reduced_imgs.reduceColumns(ee.Reducer.toList(2), ['date','mean']).values().get(0)
            df = pd.DataFrame(nested_list.getInfo(), columns=['date','mean'])
            t2 = time.time()
            print('Descarga OK', 'tiempo', round((t2-t1)/60,2), 'minutos')
            dl = True
            break
        except:
            print('Intento fallido')
            dl = False
            
    df.set_index('date',inplace=True)
    serie = df['mean']
    serie.index = pd.to_datetime(serie.index)
    serie.rename(variable_name,inplace=True)
    Serie = serie
    # if dataset_str == 'GPM':
    #     Serie = Serie * 0.5
    #     Serie = Serie.resample('D').sum()
    # elif dataset_str == 'ERA5dayP':
    #     Serie = Serie * 1000
        
    # elif dataset_str in ['ERA5dayT', 'FLDASdayT']:
    #     Serie = Serie - 273.15
        
    # elif dataset_str == 'GLDAS21_ta':
    #     Serie = Serie - 273.15
    #     Serie = Serie.resample('D').mean()
        
    # elif dataset_str == 'GLDAS21_pres':
    #     Serie = Serie.resample('D').mean()
        
    # elif dataset_str == 'GLDAS21_hum':
    #     Serie = Serie.resample('D').mean()
        
    # elif dataset_str == 'GLDAS21_ET':
    #     Serie = Serie.resample('D').mean()
        
    # elif dataset_str == 'ERA5hourT2m':
    #     Serie = Serie.resample('D').mean()
    #     Serie = Serie - 273.15
        
    # elif dataset_str == 'CFSV2_T2m':
    #     Serie = Serie.resample('D').mean()
    #     Serie = Serie - 273.15
    
    return Serie


def filter_multipolygon(geometry, percentage):
    if geometry.geom_type == 'MultiPolygon':
        max_area = 0
        subpoly_max = None
    
        for subpoly in geometry:
            subpoly_Area = subpoly.area
            if subpoly_Area > max_area:
                subpoly_max = subpoly
                max_area = subpoly_Area
        
        subpoly_max = subpoly_max.simplify(tolerance = percentage)
    else:
        subpoly_max = geometry
        
    return subpoly_max

def daterangesplit(datestr1,datestr2,dataset_freq):
    
    dt1 = pd.to_datetime(datestr1)
    dt2 = pd.to_datetime(datestr2)
    
    delta = pd.Timedelta(88, 'D')
    
    datesVector = []
    
    if (dt2-dt1) > delta:
    
        if dataset_freq in ['30-min', 'hourly', '3-hourly', '6-hourly']:
                dt_range = pd.date_range(start=datestr1,end=datestr2,
                                         freq = '1MS',
                                         closed = None)
                
        elif dataset_freq == 'daily':
            dt_range = pd.date_range(start=datestr1,end=datestr2, freq = '1MS',
                                     closed = None)
        else:
            pass
        
        dt_range = list(dt_range.astype(str).values)
        
        if datestr1 != dt_range[0]:
            dt_range.insert(0,datestr1)
        else:
            pass
            
        if datestr2 != dt_range[-1]:
            dt_range.append(datestr2)
        else:
            pass
        
        for a, b in zip(dt_range[:-1], dt_range[1:]):
            datesVector.append([a,b])
    
    else:
        
        datesVector.append([datestr1,datestr2])
        
    return datesVector
    

def catchment_gdf_TS(gdf, dataset_str, simplify = 0.0):
    gdf = gdf.to_crs('EPSG:4326')
    global_time1 = time.time()
    daterange = dates[dataset_str]
    dt_1 = pd.to_datetime(daterange[0])
    dt_2 = pd.to_datetime(daterange[1])
    dt_range = pd.date_range(start=dt_1,end=dt_2, freq = 'YS')
    dt_range2 = dt_range[1:]
    dt_range2 = dt_range2.append(pd.DatetimeIndex([dt_2]))
    datesVector = []
    # Generate datepair array
    for a,b in zip(dt_range.astype(str).values, dt_range2.astype(str).values):
        datesVector.append([a,b])
    
    # Nivel 0: filas de geometrias en el geodataframe
    geometries_ts_array = []
    for idx, geometry_row in enumerate(gdf.geometry):
        simplified_geometry = filter_multipolygon(geometry_row, simplify)
        series_array = []
        for datepair in datesVector:
            print('Descargando para rango:', datepair)
            print('Descargando geometria:', idx)
            serie = polygon_sample(simplified_geometry, dataset_str, datepair[0],
                                 datepair[1])
            serie.rename(str(idx), inplace=True)
            series_array.append(serie)
        geometry_ts = pd.concat(series_array)
        geometry_ts.sort_index(inplace=True)
        geometries_ts_array.append(geometry_ts)
    
    gdf_ts_dataframe = pd.concat(geometries_ts_array, axis=1)
    global_time2 = time.time()
    
    print('Proceso realizado en', round((global_time2-global_time1)/60,2),
          'minutos')
    return gdf_ts_dataframe

def catchment_gdf_TS_2(gdf, dataset_str, variable,
                       datestr1 = None, datestr2 = None,
                       simplify = 0.0):
    
    # Transformar geodataframe a EPSG:4326
    gdf = gdf.to_crs('EPSG:4326')
    
    # Timing global
    global_time1 = time.time()
    
    # Crea la clase dataset con los atributos segun el diccionario
    connection = dataset(dic_productos[dataset_str])
    
    # Chequeando errores de rango de fechas
    if (datestr1) == None and (datestr2) == None: 
        datestr1 = connection.dates[0]
        datestr2 = connection.dates[1]
    elif (datestr1) == None and (datestr2) != None:
        datestr1 = connection.dates[0]
    elif (datestr1) != None and (datestr2) == None:
        datestr2 = connection.dates[1]
        
    str_error_left = 'Fecha de inicio fuera de rango: '\
        + connection.dates[0] + ' a ' + connection.dates[1]
    str_error_right = 'Fecha de termino fuera de rango: '\
        + connection.dates[0] + ' a ' + connection.dates[1]
    if datestr1 != None and datestr2 != None:
        if pd.to_datetime(datestr1) < pd.to_datetime(connection.dates[0]) \
            or pd.to_datetime(datestr1) > pd.to_datetime(connection.dates[1]):
                raise ValueError(str_error_left)
        if pd.to_datetime(datestr2) < pd.to_datetime(connection.dates[0]) \
            or pd.to_datetime(datestr2) > pd.to_datetime(connection.dates[1]):
                raise ValueError(str_error_right)
                
    dataset_freq = connection.tres
    
    # Obteniendo vector de fechas dependiendo de fecha inicial, final y fre_
    # cuencia
    datesVector = daterangesplit(datestr1,datestr2,dataset_freq)
    
    # Nivel 0: filas de geometrias en el geodataframe
    geometries_ts_array = []
    for idx, geometry_row in enumerate(gdf.geometry):
        simplified_geometry = filter_multipolygon(geometry_row, simplify)
        series_array = []
        for datepair in datesVector:
            print('Descargando para rango:', datepair)
            print('Descargando geometria:', idx)
            serie = polygon_sample2(simplified_geometry,
                                    connection,
                                    variable,
                                    datepair[0],
                                 datepair[1])
            serie.rename(str(idx), inplace=True)
            series_array.append(serie)
        geometry_ts = pd.concat(series_array)
        geometry_ts.sort_index(inplace=True)
        geometries_ts_array.append(geometry_ts)
    
    gdf_ts_dataframe = pd.concat(geometries_ts_array, axis=1)
    global_time2 = time.time()
    
    print('Proceso realizado en', round((global_time2-global_time1)/60,2),
          'minutos')
    return gdf_ts_dataframe

if __name__=='__main__':
    print('hola')
else:
    pass
# jfuentes@scmaipo.cl
# rvigneaux@canalmallarauco.cl
# Presidente Tercera Sección río Mapocho: Nicolás Valdés:  nvaldes@valvalle.cl
# jcarvallo@carvalloingenieros.cl
# agomez@scmaipo.cl



