# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 09:41:57 2021

@author: Carlos
"""

import pandas as pd
import os
import datetime
import snowForecast
import numpy as np

def readSnow(ruta_n):
    # cargar las coberturas nivales
    global last_day

    df_n = pd.DataFrame([])
    for filename in os.listdir(ruta_n):
        if 'DailySnowCover' in filename:
            df_n = pd.concat([df_n, pd.read_csv(os.path.join(ruta_n,filename), index_col = 0, parse_dates = True)])
    df_n.sort_index(axis = 0, inplace = True)
    df_n = df_n.loc[df_n.index.year >= 2020]
    last_day = df_n.index[-1]

    # cargar sobre coberturas glaciales
    df_g = pd.DataFrame([])
    for filename in os.listdir(ruta_n):
        if 'DailyGlacialCover' in filename:
            df_g = pd.concat([df_g, pd.read_csv(os.path.join(ruta_n,filename), index_col = 0, parse_dates = True)])
    df_g.sort_index(axis = 0, inplace = True)
    df_g = df_g.loc[df_g.index.year >= 2020]      

    df_n.dropna(inplace = True)
    
    return df_n, df_g.loc[df_n.index]

def summerDays(last_day, master):
        # calcular los días de verano
    summer_d = pd.DataFrame([], index = pd.date_range('2000-01-01', last_day), columns = ['day'])
    summer_d['day'] = 0
    summer_d.loc[summer_d.index.month.isin([1,2,3,12]),'day'] = 1
    marzo = summer_d.loc[summer_d.index.month == 3]
    for ind,row in marzo.iterrows():
        if ind.day > 21:
            summer_d.loc[ind,'day'] = 0
    diciembre = summer_d.loc[summer_d.index.month == 12]
    for ind,row in diciembre.iterrows():
        if ind.day < 21:
            summer_d.loc[ind,'day'] = 0
    master.loc[summer_d.index, 'summer'] = summer_d['day'].values
    
    return master

def readPp(ruta_pp, master, last_day):
    # procesar precipitaciones
    df_pp = pd.read_csv(ruta_pp, index_col = 0, parse_dates = True)
    df_pp = df_pp.loc[(df_pp.index.year >= 2021) & (df_pp.index <= last_day)]
    cols_pp = [x for x in master.columns if 'Pp_' in x]
    master.loc[df_pp.index, cols_pp] = df_pp.values
    
    return master

def readT(ruta_t, master, last_day):

    # procesar temperaturas
    df_t = pd.read_csv(ruta_t, index_col = 0, parse_dates = True)
    df_t = df_t.loc[(df_t.index.year >= 2000) & (df_t.index <= last_day)]
    cols_t = [x for x in master.columns if 'T_' in x]
    master.loc[df_t.index, cols_t] = df_t.values

    return master

def matchPp(pp_, lday, df_h):
    """
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    master_ : TYPE
        DESCRIPTION.
    last_date : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    # seleccionar sólo los datos medidos    
    pp_ = pp_.loc[pp_.index <= lday]
    
    # año de pronóstico
    if lday.strftime('%m-%d') > '03-31':    
        forecast_year = pp_.index[-1].year      
    else: 
        forecast_year = pp_.index[-1].year-1    
        
    # calcular la precipitación media de la cuenca
    pp_mean = pd.DataFrame(np.sum(pp_.mul(df_h['area'].values), axis = 1) / df_h['area'].sum())
    
    first_date = pd.to_datetime(str(forecast_year)+'-04-01')        
    last_ppmean = pp_mean.loc[(pp_mean.index >= first_date ) & (pp_mean.index <= lday)]
    len_last_ppmean = len(last_ppmean.index)
    
    # años anteriores
    previous_years = list(dict.fromkeys(pp_mean.index.year))[:-1]
        
    # calcular la precipitación acumulada de los años anteriores
    ppmean_registry = pd.DataFrame([], index = previous_years, columns = ['ppm'])
    
    # iterar sobre los años
    for yr in previous_years:
        start =  pd.to_datetime(str(yr)+'-04-01')    
        end = start + datetime.timedelta(days = len_last_ppmean-1)   
        ppmean_registry.loc[yr,'ppm'] = float(pp_mean.loc[pd.date_range(start,end)].sum().values[0])

    df_pp_30 = ppmean_registry['ppm'].quantile(1-0.3)
    
    # if (last_ppmean.sum().values >= df_pp_30) | (forecast_year in [2020,2021]):
    if last_ppmean.sum().values >= df_pp_30:
        return 2000
    else:
        return 2019

def completarMaster(master, lday, df_h):
    
    # extraer la precipitacion 
    pp = master[[x for x in master.columns if 'Pp_' in x]]
       
    # completar los parámetros
    par = [x for x in master.columns if ('Zone' not in x) & ('Pp_' not in x) & ('T_' not in x) & ('Measured Discharge' not in x)]
    last_par = master['Recess_X']
    last_par.dropna(inplace = True)
    
    # completar los parametros del predictivo junto a los dias de años bisiestos
    idx_missing = pd.date_range(last_par.index[-1]+datetime.timedelta(days = 1), master.index[-1], freq = '1d' )
    yrs_missing = list(dict.fromkeys(idx_missing.year))
    
    # iterar sobre los años hidrologicos
    for yr in yrs_missing:
        
        # mínimo entre el ultimo día de los parámetros faltantes y el último día del año hidrológico
        last_day_yr = min(pd.to_datetime(str(yr+1)+'-03-31'), idx_missing[-1])
         
        # determinar si el año hasta las observaciones es seco o húmedo
        yr_param = matchPp(pp, last_day_yr, df_h)
    
        # tengo que hacer el for por si hay años bisiestos
        if min(idx_missing).strftime('%m-%d') > '03-31':
            idx_date = idx_missing[(idx_missing <= last_day_yr) & (idx_missing >= pd.to_datetime(str(yr)+'-04-01'))]
        else:
            idx_date = idx_missing[(idx_missing <= last_day_yr) & (idx_missing >= pd.to_datetime(str(yr-1)+'-04-01'))]            
        for date in idx_date: 
            yr_delta = date.year-idx_date.year[0]
            
            master.loc[date, par] = master.loc[pd.to_datetime(str(yr_param+yr_delta)+'-'+str(date.month)+'-'+str(date.day)), par].values
        
        # identificar los días bisiestos a completar
        feb_bisiesto = [f for f in idx_date if (f.month == 2) & (f.day == 29)]
        
        for feb in feb_bisiesto:
            yr_delta = feb.year-idx_date.year[0]
            if yr_param < 2018:
                master.loc[feb, par] = master.loc[pd.to_datetime(str(2000+yr_delta)+'-02-29'), par].values
            else:
                master.loc[feb, par] = master.loc[pd.to_datetime(str(2019+yr_delta)+'-02-29'), par].values
        
    return master

def SRM_master(folder):
    """
    

    Parameters
    ----------
    ruta_pp : str
        ej. ruta_pp = r'E:\CIREN\OneDrive - ciren.cl\Of hidrica\AOHIA_ZC\Etapa 3\SRM\Datos\Cuencas\Mapocho_Los_Almendros\Datos_Intermedia\MLAL_pr_EB_250_method_N.csv'

    ruta_t : str
        ej.  ruta_t = r'E:\CIREN\OneDrive - ciren.cl\Of hidrica\AOHIA_ZC\Etapa 3\SRM\Datos\Cuencas\Mapocho_Los_Almendros\Datos_Intermedia\MLAL_t2m_EB_250.csv'
    ruta_n : str
        ej.   ruta_n = r'E:\CIREN\OneDrive - ciren.cl\Of hidrica\AOHIA_ZC\Etapa 3\SRM\Datos\Cuencas\Mapocho_Los_Almendros\Datos_Intermedia'
    Returns
    -------
    None.

    """
    
 # ============================================================================
 #                          archivo master de validacion 
 # ----------------------------------------------------------------------------
     # rutas
    path_q = os.path.join(folder,'Caudales',r'Caudales.csv')
    ruta_n = os.path.join(folder,'Nieve')
    root = os.path.join(folder,'SRM')
    ruta_pp = os.path.join(folder,'Precipitacion',r'precipitacion_forecast.csv')
    ruta_t = os.path.join(folder,'Temperatura',r'temperatura_forecast.csv')

    # leer caudales del usuario
    q_obs = pd.read_csv(path_q,index_col = 0, parse_dates = True, dayfirst = True) 
    q_obs.dropna(inplace = True)
        
    # leer archivo master predictivo
    if os.path.isfile(os.path.join(root,'Inputs',r'Master.csv')):

        #último archivo predictivo
        master_val = pd.read_csv(os.path.join(root,'Inputs',r'Master.csv'), index_col = 0, parse_dates = True)
                
    else:
        # si es la primera simulacion predictiva, comenzar desde los datos del modelo validado
        print('El archivo Master.csv no se encuentre en la carpeta Inputs')
        return
       
    # leer cobertura de nieves
    df_n, df_g = readSnow(ruta_n)
    
    # extender el master de validacion
    idx = pd.date_range(master_val.index[-1]+datetime.timedelta(days = 1), df_n.index[-1], freq = '1d')
    
    complemento = pd.DataFrame([], index = idx, columns = master_val.columns)
    master_val = master_val.append(complemento)
    
    # seleccionar las columnas que corresponen a fraccion cubierta nivale
    cols_SCA = [x for x in master_val.columns if ('Zone' in x) & ('.' not in x)]
    cols_GCA = [x for x in master_val.columns if ('Zone' in x) & ('.' in x)]
        
    # ingresar la nieves
    master_val.loc[df_n.index,cols_SCA] = df_n.values
    master_val.loc[df_g.index,cols_GCA] = df_g.values
            
    # agregar caudales del usuario
    idx = idx.intersection(q_obs.index)
    master_val.loc[idx, 'Measured Discharge' ] = q_obs.loc[idx].values
    # master_val.to_csv(path_master_val)
        
    # último día de la validacion
    last_day = df_n.index[-1]

    # calcular los días de verano
    master_val = summerDays(last_day, master_val)
    
    # # leer precipitaciones del usuario
    df_pp = pd.read_csv(ruta_pp, index_col = 0, parse_dates = True)
    df_pp_preforecast = df_pp.loc[(df_pp.index.year >= 2000) & (df_pp.index <= last_day)]
    cols_pp = [x for x in master_val.columns if 'Pp_' in x]
    master_val.loc[df_pp_preforecast.index, cols_pp] = df_pp_preforecast.values
    
    # # leer temperaturas del usuario
    df_t = pd.read_csv(ruta_t, index_col = 0, parse_dates = True)
    df_t_preforecast = df_t.loc[(df_t.index.year >= 2000) & (df_t.index <= last_day)]
    cols_t = [x for x in master_val.columns if 'T_' in x]
    master_val.loc[df_t_preforecast.index, cols_t] = df_t_preforecast.values
    
    # leer curva hipsométrica de la cuenca
    df_hypso = pd.read_csv(os.path.join(root,'Inputs',r'Hypso.csv'), index_col = 0)
    
    # completar los parametros que faltan del periodo de validacion
    master_val = completarMaster(master_val, last_day, df_hypso)
    
    # guardar el master del periodo de validacion
    master_val.to_csv(os.path.join(root,'Inputs',r'Master.csv'))
    pd.DataFrame(df_n.index).to_csv(os.path.join(root,'Inputs',r'LastDateVal.csv'), index = None)
    
 # ============================================================================
 #                          archivo master predictivo 
 # ----------------------------------------------------------------------------  
 
    # crear el archivo master del predictivo
    master_pred = snowForecast.snow_forecast(root)
    
    # completar los parámetros del año a  pronosticar
    master_pred = completarMaster(master_pred, master_pred.index[-1], df_hypso)
    
    # # leer precipitaciones del usuario
    df_pp = df_pp.loc[df_pp.index <= master_pred.index[-1]]
    df_pp = df_pp.loc[df_pp.index.year > 2000]
    master_pred.loc[df_pp.index, cols_pp] = df_pp.values
    
    # # leer temperaturas del usuario
    df_t = df_t.loc[df_t.index <= master_pred.index[-1]]
    df_t = df_t.loc[df_t.index.year > 2000]
    master_pred.loc[df_t.index, cols_t] = df_t.values
    
    # guardar el archivo master predictivo
    master_pred.to_csv(os.path.join(root,'Inputs',r'Master.csv'))

    