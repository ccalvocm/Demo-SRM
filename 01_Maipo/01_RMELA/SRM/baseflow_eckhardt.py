# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 21:09:21 2021

@author: Carlos
"""

import eckhardt
import pandas as pd
import datetime
import numpy as np

def baseflow(strflow,alpha,beta,bf):
        
    # calcular el caudal total medio mensual para determinar el flujo base
    strflow = pd.DataFrame(strflow, index = pd.date_range('2000-01-01',pd.to_datetime('2000-01-01')+datetime.timedelta(days=len(strflow)-1), freq = '1d') )
    date_end = strflow.index[-1]
    fill_value = strflow.loc[(strflow.index.month == date_end.month) & (strflow.index.year == date_end.year)].min().values
    idx = pd.date_range(strflow.index[0],str(date_end.year)+'-'+str(date_end.month)+'-'+str(date_end.days_in_month), freq = '1d')
    strflow = strflow.reindex(idx, fill_value=fill_value[0])
    # calcular el baseflow medio mensual
    df_BaseFlow = pd.DataFrame(bf, index = pd.date_range('2000-01-01',pd.to_datetime('2000-01-01')+datetime.timedelta(days=len(bf)-1), freq = '1d') )
    
    # baseq = eckhardt.eckhardt(strflow, alpha, beta, init_value=None, window=7)
    baseq = eckhardt.naive_eckhardt(strflow, alpha, beta)
    
    # asignar fechas al flujo base mensual
    df_baseq = pd.DataFrame(baseq, index = pd.date_range('2000-01-01',date_end, freq = '1d') )
    # resample del flujo base mensual a diario
    baseq_day = df_baseq.reindex(pd.date_range('2000-01-01',date_end,freq = '1d'), method='nearest')
    # tolerancia como MSE del baseflow actual y anterior 
    tol = np.sqrt(np.sum(((df_baseq.values-df_BaseFlow.values)/df_baseq.values))**2./len(df_baseq.values))
    
    return baseq_day.values , tol
    
if __name__ == '__main__':
    pass