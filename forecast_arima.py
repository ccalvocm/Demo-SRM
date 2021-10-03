#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 14:41:47 2021

@author: faarrosp
"""

import os
import pandas as pd
import pmdarima as pm
from pmdarima import model_selection
import matplotlib.pyplot as plt
import numpy as np

def inverse_diff(differentiated, original, interval=1, unit = 'D'):
    val = []
    idx = []
    for t in differentiated.index:
        # print(t)
        dt = pd.Timedelta(value = interval, unit = unit)
        idx.append(t)
        # print(t-dt)
        val.append(differentiated.loc[t] + original.loc[t-dt])
    inverted_series = pd.Series(data=val,index = idx)
    return inverted_series

path = ['/home', 'faarrosp','Documents','GitHub',
        'Demo-SRM','01_Maipo','01_RMELA',
        'Temperatura', 'temperatura_actual.csv']

path_tmed = os.path.join(*path)

df = pd.read_csv(path_tmed, index_col=0, parse_dates=(True))

ts = df['0']

train, test = model_selection.train_test_split(ts, train_size=0.8)

###############################################################################
# Differentiate series

trainD = train.diff(365).dropna()
testD = test.diff(365).dropna()

# #############################################################################
# Fit with some validation (cv) samples
arima = pm.ARIMA(order=(7, 0, 1))
arima.fit(trainD)

# Now plot the results and the forecast for the test set
preds, conf_int = arima.predict(n_periods=test.shape[0],
                                return_conf_int=True)

# generate predictions as Pandas Series
preds = pd.Series(preds, index=test.index)
conf_int_lower = pd.Series(conf_int[:,0], index = test.index)
conf_int_upper = pd.Series(conf_int[:,1], index = test.index) 

# apply inverse difference to get real values of prediction
predsINV = inverse_diff(preds,ts,interval=365)




fig, axes = plt.subplots(2, 1, figsize=(12, 8))
x_axis = np.arange(train.shape[0] + preds.shape[0])
axes[0].plot(x_axis[:train.shape[0]], train, alpha=0.75)
axes[0].scatter(x_axis[train.shape[0]:], preds, alpha=0.4, marker='o')
axes[0].scatter(x_axis[train.shape[0]:], test, alpha=0.4, marker='x')
axes[0].fill_between(x_axis[-preds.shape[0]:], conf_int[:, 0], conf_int[:, 1],
                     alpha=0.1, color='b')

# fill the section where we "held out" samples in our model fit

axes[0].set_title("Train samples & forecasted test samples")