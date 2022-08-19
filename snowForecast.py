# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:23:20 2021

@author: Carlos
"""
#========================================================================== 
#                           cargar librerias
#==========================================================================
import pandas as pd
import datetime
from statsmodels.tsa.arima.model import ARIMA
from dateutil.relativedelta import relativedelta
import os
import numpy as np
import hydroeval
import warnings
warnings.filterwarnings('ignore')

# funciones

def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i-interval]
        diff.append(value)
    return np.array(diff)

def inverse_difference(history, yhat, interval=1):
	return yhat + history.iloc[:-interval]

def inverse_diff(differentiated, original, interval=1, unit = 'D'):
    val = []
    idx = []
    for t in differentiated.index:
        dt = pd.Timedelta(value = interval, unit = unit)
        idx.append(t)
        val.append(differentiated.loc[t] + original.loc[t-dt])
    inverted_series = pd.Series(data=val,index = idx)
    return inverted_series

def matchSnow(master_, last_date, df_h, cols):
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
    
    # año de pronóstico
    forecast_year = master_.index[-1].year-1
    
    # seleccionar sólo los datos medidos    
    master_ = master_.loc[master_.index <= last_date]
    
    # calcular el área cubierta de nieve de la cuenca
    wSCAhi = pd.DataFrame(np.sum(master_[cols].mul(df_h['area'].values), axis = 1) / df_h['area'].sum())
    
    first_date = pd.to_datetime(str(forecast_year)+'-04-01')        
    last_CDC = wSCAhi.loc[(wSCAhi.index >= first_date ) & (wSCAhi.index <= last_date)]
    len_last_cover = len(last_CDC.index)
    
    # años anteriores
    previous_years = list(dict.fromkeys(wSCAhi.index.year))[:-2]
    
    # fig, ax = plt.subplots(1)
    # comparar las curvas de agotamiento acumuladas CDC de los años anteriores
    
    rmse = np.inf
    best_rmse = np.inf
    best_year = 2019
    
    # iterar sobre los años
    for yr in previous_years:
        start =  pd.to_datetime(str(yr)+'-04-01')    
        end = start + datetime.timedelta(days = len_last_cover-1)   
        historical_CDC =  wSCAhi.loc[pd.date_range(start,end)]
        rmse = hydroeval.rmse(historical_CDC.values, last_CDC.values)
        if best_rmse > rmse:
            best_rmse = rmse
            best_year = yr
    
    # devolver el mejor año
    return best_year
    

def pronostico_ARMA(df, dias, orden):

    # Parameters
    # ----------
    # df : Pandas DataFrame
    #     dataframe de nieve medida.
    # dias : int
    #     dias del periodo predictivo.
    # orden : tuple
    #     orden del ARMA.

    # Returns
    # -------
    # predictions : Pandas DataFrame
    #     cubierta nival pronosticada.
    
    model = ARIMA(df, 
                order = orden, 
                seasonal_order = (0,0,0,365))
    # fit model
    result = model.fit(method='innovations_mle', low_memory=True, cov_type='none')

    # make prediction
    predictions = result.predict(1, dias,
                                 typ = 'levels')
    
    return predictions

def snow_forecast(root):

    # Parameters
    # ----------
    # years : int
    #     años a modelar, ejemplo 20002020.
    # root : str
    #     directorio raíz.
    # Returns
    # -------
    # None.    

    #construir las coberturas del predictivo
    years_train =  10
    
    # leer el arhcivo master del periodo de pronostico
    
    # leer archivo master predictivo
    if os.path.isfile(os.path.join(root,'Inputs',r'Master.csv')):

        #último archivo predictivo
        master = pd.read_csv(os.path.join(root,'Inputs',r'Master.csv'), index_col = 0, parse_dates = True)
                
    else:
        # si es la primera simulacion predictiva, comenzar desde los datos del modelo validado
        print('El archivo Master.csv no se encuentre en la carpeta Inputs')
        return
        
    # cargar la curva hipsométrica
    df_hypso = pd.read_csv(os.path.join(root,'Inputs',r'Hypso.csv'), index_col = 0)
    
    # leer última fecha de las imágenes modis
    last_date = pd.read_csv(os.path.join(root,'Inputs',r'LastDateVal.csv'), index_col = 0, parse_dates = True).index[-1]
        
    # asignar las fechas
    master = master.loc[master.index <= last_date]

    last_snow = master[[x for x in master.columns if ('Zone' in x) & ('.' not in x)]]
    last_snow.dropna(inplace = True)
    
    if last_date.strftime('%m-%d') == '03-31':   
        print('El período predictivo de la temporada de riego debe ser mayor o igual a 1 dia')
        return None        
    if last_date.strftime('%m-%d') > '03-31':    
        idx = pd.date_range(last_date+datetime.timedelta(days = 1), pd.to_datetime(str(last_date.year+1)+'-03-31'), freq = '1d')        
    else: 
        idx = pd.date_range(last_date+datetime.timedelta(days = 1), pd.to_datetime(str(last_date.year)+'-03-31'), freq = '1d')
    
    # extender el archivo master hasta el pronóstico
    complemento = pd.DataFrame([], index = idx, columns = master.columns)
    master = master.append(complemento)
    
    # cargar coberturas de nieve y glaciares
    cols_SCA = [x for x in master.columns if ('Zone' in x) & ('.' not in x)]
    SCA = master[cols_SCA]         # Snow Covered Area (%) 
    cols_GCA = [x for x in master.columns if ('Zone' in x) & ('.' in x)]
    GCA = master[cols_GCA]     # Glacier Covered Area (%)

    # año que mejor se ajusta a la nieve acumulada
    best_year_s = matchSnow(master.loc[master.index.year >= last_date.year-years_train], last_date, df_hypso, cols_SCA)      
  
    for ind, col in enumerate(SCA.columns):
        
        # coberturas de nieve para el periodo de entrenamiento
        idx_s = pd.date_range(last_date-relativedelta(years=(last_date.year - best_year_s)), last_date,freq = '1d')
        if (SCA.loc[idx_s,col] > 0).any():
            
            # realizar el pronóstico
            pronostico_nieve = pronostico_ARMA(SCA.loc[idx_s,col], last_date, (2,1,0))
            pronostico_nieve[pronostico_nieve < 0] = 0
            pronostico_nieve[pronostico_nieve > 1] = 1
            
            # guardar el pronóstico
            idx2 = pd.date_range(pd.to_datetime(pd.to_datetime(last_date)+datetime.timedelta(days = 1)), master.index[-1], freq = '1d')
            master.loc[idx2,col] = pronostico_nieve.iloc[:len(idx2)].values
        
        # coberturas de glaciares
        idx_g = pd.date_range(pd.to_datetime(last_date)-relativedelta(years=(last_date.year - best_year_s)),pd.to_datetime(last_date),freq = '1d')
        if (GCA.loc[idx_g,col+'.1'] > 0).any():
            
            # realizar el pronóstico
            pronostico_glaciares = pronostico_ARMA(GCA.loc[idx_g,col+'.1'], last_date, (2,1,0))
            pronostico_glaciares[pronostico_glaciares < 0] = 0
            pronostico_glaciares[pronostico_glaciares > 1] = 1
            
            # guardar el pronóstico
            master.loc[idx2,col+'.1'] = pronostico_glaciares.iloc[:len(idx2)].values
    
    master[cols_SCA] = master[cols_SCA].fillna(0)
    master[cols_GCA] = master[cols_GCA].fillna(0)
   
    return master
