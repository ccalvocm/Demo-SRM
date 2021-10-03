#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 02:53:16 2021

@author: faarrosp
"""

## for data
import os
import pandas as pd
import numpy as np## for plotting
import matplotlib.pyplot as plt
import seaborn as sns## for statistical tests
import scipy
import statsmodels.formula.api as smf
import statsmodels.api as sm## for machine learning
from sklearn import model_selection, preprocessing,\
    feature_selection, ensemble, linear_model, metrics,\
        decomposition## for explainer
# from lime import lime_tabular

def utils_recognize_type(dtf, col, max_cat=20):
    if (dtf[col].dtype == "O") | (dtf[col].nunique() < max_cat):
        return "cat"
    else:
        return "num"

def define_rainfall_event_binary(x):
    if x > 0.1:
        return 1
    else:
        return 0

def remove_duplicated_indices_from_dataframe(df):
    df_new = df[~df.index.duplicated(keep='first')]
    return df_new

def set_common_index_to_dataframe(df,index):
    df_new = df.loc[index,:].copy()
    return df_new

def classify_precipitation_dataframe(path):
    # import all relevant datasets
    path_precip = os.path.join(path, 'Precipitacion',
                               'precipitacion_actual.csv')
    path_temper = os.path.join(path, 'Temperatura',
                               'temperatura_actual.csv')
    path_presio = os.path.join(path, 'Predictores_precipitacion',
                               'presion_actual.csv')
    path_humeda = os.path.join(path, 'Predictores_precipitacion',
                               'humedad_actual.csv')
    path_viento = os.path.join(path, 'Predictores_precipitacion',
                               'viento_actual.csv')
    path_evapot = os.path.join(path, 'Predictores_precipitacion',
                               'evapotranspiracion_actual.csv')
    
    # load all datasets into dataframes
    df_precip = pd.read_csv(path_precip, index_col=0, parse_dates=True)
    df_temper = pd.read_csv(path_temper, index_col=0, parse_dates=True)
    df_presio = pd.read_csv(path_presio, index_col=0, parse_dates=True)
    df_humeda = pd.read_csv(path_humeda, index_col=0, parse_dates=True)
    df_viento = pd.read_csv(path_viento, index_col=0, parse_dates=True)
    df_evapot = pd.read_csv(path_evapot, index_col=0, parse_dates=True)
    
    dataframes = [df_precip, df_temper, df_presio,
                  df_humeda, df_viento, df_evapot]
    
    # remove any duplicated indices from every dataframe
    for df in dataframes:
        df = remove_duplicated_indices_from_dataframe(df)
        
    # set all dataframes to the same index    
    indices = [set(x.index) for x in dataframes]
    indices = set.intersection(*indices)
    indices = sorted(list(indices))
    
    
    df_precip = df_precip.loc[indices,:].copy()
    df_temper = df_temper.loc[indices,:].copy()
    df_presio = df_presio.loc[indices,:].copy()
    df_humeda = df_humeda.loc[indices,:].copy()
    df_viento = df_viento.loc[indices,:].copy()
    df_evapot = df_evapot.loc[indices,:].copy()
        
    
    # This process must be performed for each column (band)
    for col in df_precip.columns[:1]:
        ts_precip = df_precip[col].rename('precip').\
            apply(define_rainfall_event_binary)
        ts_temper = df_temper[col].rename('temper')
        ts_presio = df_presio[col].rename('presio')
        ts_humeda = df_humeda[col].rename('humeda')
        ts_viento = df_viento[col].rename('viento')
        ts_evapot = df_evapot[col].rename('evapot')
        ts_mescat = pd.Series(ts_temper.index.month.values,
                              index=ts_temper.index, name='month')
        dtf = pd.concat([ts_precip, ts_temper, ts_presio, ts_humeda,
                         ts_viento, ts_evapot, ts_mescat], axis=1)
    
    
        ###################################################
        # Analysis for categorical and numerical variables
        # dic_cols = {col:utils_recognize_type(dtf, col, max_cat=20) for col in dtf.columns}
        # heatmap = dtf.isnull()
        # for k,v in dic_cols.items():
        #     if v == "num":
        #         heatmap[k] = heatmap[k].apply(lambda x: 0.5 if x is False else 1)
        #     else:
        #         heatmap[k] = heatmap[k].apply(lambda x: 0 if x is False else 1)
        # sns.heatmap(heatmap, cbar=False).set_title('Dataset Overview')
        # plt.show()
        # print("\033[1;37;40m Categerocial ", "\033[1;30;41m Numeric ", "\033[1;30;47m NaN ")
        
        ###################################################
        # split data between train and test
        dtf_train, dtf_test = model_selection.train_test_split(dtf,
                                                               train_size=0.7)
        
        ## print info
        print("X_train shape:", dtf_train.drop("precip",axis=1).shape,
              "| X_test shape:", dtf_test.drop("precip",axis=1).shape)
        print("y_train mean:", round(np.mean(dtf_train["precip"]),2),
              "| y_test mean:", round(np.mean(dtf_test["precip"]),2))
        print(dtf_train.shape[1], "features:",
              dtf_train.drop("precip",axis=1).columns.to_list())
        
        
        ## create dummy
        dummy = pd.get_dummies(dtf_train["month"], 
                               prefix="month",drop_first=True)
        dtf_train= pd.concat([dtf_train, dummy], axis=1)
        print( dtf_train.filter(like="month", axis=1).head() )
        
        ## drop the original categorical column
        dtf_train.drop("month", axis=1, inplace=True)
        dtf_train.sort_index(axis=0,inplace=True)
        
        
        # # scale the numeric variables
        scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
        X = scaler.fit_transform(dtf_train.drop("precip", axis=1))
        dtf_scaled= pd.DataFrame(X, columns=dtf_train.drop("precip", axis=1).\
                                 columns, index=dtf_train.index)
        dtf_scaled["precip"] = dtf_train["precip"]
        print(dtf_scaled.head())
        
        # Correlation matrix to know which variables to consider
        fig, ax = plt.subplots()
        corr_matrix = dtf.copy()
        for col in corr_matrix.columns:
            if corr_matrix[col].dtype == "O":
                corr_matrix[col] = corr_matrix[col].factorize(sort=True)[0]
                
        corr_matrix = corr_matrix.corr(method="pearson")
        sns.heatmap(corr_matrix, vmin=-1., vmax=1., annot=True, fmt='.2f',
                    cmap="YlGnBu", cbar=True, linewidths=0.5)
        plt.title("pearson correlation")

        
        
        
        # # LASSO regularization (another way to find out relevant variables)
        #     # rename variables to make it easier
            
        dtf.rename({'precip': 'Y'}, axis=1, inplace=True)
        dtf_train.rename({'precip': 'Y'}, axis=1, inplace=True)
        # dtf_test.rename({'precip': 'Y'}, axis=1, inplace=True)
        dtf_scaled.rename({'precip': 'Y'}, axis=1, inplace=True)
        
        dtf_train = dtf_scaled.copy()
        
        # now perform regularization
        X = dtf_train.drop("Y", axis=1).values
        y = dtf_train["Y"].values
        feature_names = dtf_train.drop("Y", axis=1).columns
        
        ## Anova
        selector = feature_selection.SelectKBest(score_func=  
                        feature_selection.f_classif, k=10).fit(X,y)
        anova_selected_features = feature_names[selector.get_support()]
        
        ## Lasso regularization
        selector = feature_selection.SelectFromModel(estimator= 
                      linear_model.LogisticRegression(C=1, penalty="l1", 
                      solver='liblinear'), max_features=10).fit(X,y)
        lasso_selected_features = feature_names[selector.get_support()]
         
        ## Plot
        fig, ax = plt.subplots()
        dtf_features = pd.DataFrame({"features":feature_names})
        dtf_features["anova"] = dtf_features["features"].apply(lambda x: "anova" if x in anova_selected_features else "")
        dtf_features["num1"] = dtf_features["features"].apply(lambda x: 1 if x in anova_selected_features else 0)
        dtf_features["lasso"] = dtf_features["features"].apply(lambda x: "lasso" if x in lasso_selected_features else "")
        dtf_features["num2"] = dtf_features["features"].apply(lambda x: 1 if x in lasso_selected_features else 0)
        dtf_features["method"] = dtf_features[["anova","lasso"]].apply(lambda x: (x[0]+" "+x[1]).strip(), axis=1)
        dtf_features["selection"] = dtf_features["num1"] + dtf_features["num2"]
        sns.barplot(y="features", x="selection", hue="method", data=dtf_features.sort_values("selection", ascending=False), dodge=False)
        
        ############################################
        # Random Forest
        X = dtf_train.drop("Y", axis=1).values
        y = dtf_train["Y"].values
        feature_names = dtf_train.drop("Y", axis=1).columns.tolist()## Importance
        model = ensemble.RandomForestClassifier(n_estimators=100,
                              criterion="entropy", random_state=0)
        model.fit(X,y)
        importances = model.feature_importances_## Put in a pandas dtf
        dtf_importances = pd.DataFrame({"IMPORTANCE":importances, 
                    "VARIABLE":feature_names}).sort_values("IMPORTANCE", 
                    ascending=False)
        dtf_importances['cumsum'] =  \
                    dtf_importances['IMPORTANCE'].cumsum(axis=0)
        dtf_importances = dtf_importances.set_index("VARIABLE")
            
        ## Plot
        fig, ax = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
        fig.suptitle("Features Importance", fontsize=20)
        ax[0].title.set_text('variables')
        dtf_importances[["IMPORTANCE"]].sort_values(by="IMPORTANCE").plot(
                        kind="barh", legend=False, ax=ax[0]).grid(axis="x")
        ax[0].set(ylabel="")
        ax[1].title.set_text('cumulative')
        dtf_importances[["cumsum"]].plot(kind="line", linewidth=4, 
                                         legend=False, ax=ax[1])
        ax[1].set(xlabel="", xticks=np.arange(len(dtf_importances)), 
                  xticklabels=dtf_importances.index)
        plt.xticks(rotation=70)
        plt.grid(axis='both')
        plt.show()
        
        ############################################
        # Fit a model
        X_names = ['temper', 'month_5', 'month_6', 'month_7', 'month_8',
                   'evapot', 'humeda', 'viento', 'month_2']
        X_train = dtf_train[X_names].values
        y_train = dtf_train["Y"].values
        X_test = dtf_test[X_names].values
        y_test = dtf_test["Y"].values
        
    
    return (X_train, y_train, X_test, y_test)



if __name__ == '__main__':
    path = ['/','home','faarrosp','Documents','GitHub',
            'Demo-SRM','01_Maipo','01_RMELA']
    path = os.path.join(*path)
    print(path)
    X_train, y_train, y_test = classify_precipitation_dataframe(path)

