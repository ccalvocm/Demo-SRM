# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 22:57:13 2021

@author: Carlos
"""

import pandas as pd
import fiscalyear
fiscalyear.START_MONTH = 4    

# funciones
def agnohidrologico(date):
    year_ = date.year
    month_ = date.month
    cur_dt = fiscalyear.FiscalDate(year_, month_, 1) 
    retornar = cur_dt.fiscal_year - 1
    return int(retornar)

ruta_bf = 'baseflow_m3s.csv'
bf = pd.read_csv(ruta_bf, index_col = 0, parse_dates = True, dayfirst = True)
bf = bf[bf.index.year >= 2000]

df = bf.reindex(pd.date_range('2000-01-01','2020-03-31',freq = '1d'), method='pad')
# Río Tinguiririca en Los Briones
est = 'QRTBLBbf'
df[est].to_csv(est+'baseflow_m3s_daily.csv')

# --------------------flujo base
q_bf = pd.read_csv(est+'baseflow_m3s_daily.csv', index_col = 0, parse_dates = True)
q_bf['hidroyear'] = ''
q_bf = pd.DataFrame(q_bf.loc[(q_bf.index.year >= 2000) & (q_bf.index.year <= 2020)])
for ind, col in q_bf.iterrows():
   hidro_yr = agnohidrologico(ind)
   q_bf.loc[ind, 'hidroyear'] = hidro_yr
q_bf.reset_index(inplace = True)
q_bf[est] = q_bf[est].fillna(q_bf[est].rolling(720,center=False,min_periods=0).min())
q_bf.to_csv(est+'baseflow_m3s_daily_hidroyear.csv')