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
import statsmodels.formula.api as smf
import statsmodels.api as sm


def will_it_rain(x):
            if x>=0.5:
                return 1
            else:
                return 0

def utils_recognize_type(dtf, col, max_cat=20):
    if (dtf[col].dtype == "O") | (dtf[col].nunique() < max_cat):
        return "cat"
    else:
        return "num"

def define_rainfall_event_binary(x):
    if x > 0.1:
        return 1.0
    else:
        return 0.0

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
    for col in df_precip.columns[12:13]:
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
        dummy = pd.get_dummies(dtf["month"], 
                               prefix="month",drop_first=True)
        dtf_wdummy= pd.concat([dtf, dummy], axis=1)
        # print( dtf_wdummy.filter(like="month", axis=1).head() )
        
        ## drop the original categorical column
        dtf_wdummy.drop("month", axis=1, inplace=True)
        dtf_wdummy.sort_index(axis=0,inplace=True)
        
        # # scale the numeric variables
        scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
        X = scaler.fit_transform(dtf_wdummy.drop("precip", axis=1))
        dtf_scaled_wdummy= pd.DataFrame(X, columns=dtf_wdummy.drop("precip", axis=1).\
                                 columns, index=dtf_wdummy.index)
        dtf_scaled_wdummy["precip"] = dtf_wdummy["precip"].copy()
        dtf_scaled_wdummy.sort_index(axis=0, inplace=True)
        # print(dtf_scaled_wdummy.head())
        
        
        
        
        
        # split data between train and test
        dtf_train, dtf_test = model_selection.train_test_split(dtf_scaled_wdummy,
                                                               train_size=0.7)
        dtf_train.sort_index(axis=0, inplace=True)
        dtf_test.sort_index(axis=0, inplace=True)
        
        
        
        
        ## print info
        # print("X_train shape:", dtf_train.drop("precip",axis=1).shape,
        #       "| X_test shape:", dtf_test.drop("precip",axis=1).shape)
        # print("y_train mean:", round(np.mean(dtf_train["precip"]),2),
        #       "| y_test mean:", round(np.mean(dtf_test["precip"]),2))
        # print(dtf_train.shape[1], "features:",
        #       dtf_train.drop("precip",axis=1).columns.to_list())
        
        
        # ## create dummy
        # dummy = pd.get_dummies(dtf_train["month"], 
        #                        prefix="month",drop_first=True)
        # dtf_train= pd.concat([dtf_train, dummy], axis=1)
        # print( dtf_train.filter(like="month", axis=1).head() )
        
        # ## drop the original categorical column
        # dtf_train.drop("month", axis=1, inplace=True)
        # dtf_train.sort_index(axis=0,inplace=True)
        
        
        # # # scale the numeric variables
        # scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
        # X = scaler.fit_transform(dtf_train.drop("precip", axis=1))
        # dtf_scaled= pd.DataFrame(X, columns=dtf_train.drop("precip", axis=1).\
        #                          columns, index=dtf_train.index)
        # dtf_scaled["precip"] = dtf_train["precip"]
        # print(dtf_scaled.head())
        '''
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

        '''
        
        
        # # LASSO regularization (another way to find out relevant variables)
        #     # rename variables to make it easier
            
        # dtf.rename({'precip': 'Y'}, axis=1, inplace=True)
        # dtf_train.rename({'precip': 'Y'}, axis=1, inplace=True)
        # dtf_test.rename({'precip': 'Y'}, axis=1, inplace=True)
        # dtf_scaled_wdummy.rename({'precip': 'Y'}, axis=1, inplace=True)
        
        
        '''
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
        '''
        
        ############################################
        # Fit a model
        X_names = ['presio', 'C(month_7)', 'C(month_8)',
                    'humeda', 'viento', 'C(month_6)', 'C(month_5)',
                    'C(month_2)']
        # X_train = dtf_train[X_names].values
        # y_train = dtf_train["Y"].values
        # X_test = dtf_test[X_names].values
        # y_test = dtf_test["Y"].values
        
        ## call model
        # model = ensemble.GradientBoostingClassifier()## define hyperparameters combinations to try
        # param_dic = {'learning_rate':[0.15,0.1,0.05,0.01,0.005,0.001],      #weighting factor for the corrections by new trees when added to the model
        # 'n_estimators':[100,250,500,750,1000,1250,1500,1750],  #number of trees added to the model
        # 'max_depth':[2,3,4,5,6,7],    #maximum depth of the tree
        # 'min_samples_split':[2,4,6,8,10,20,40,60,100],    #sets the minimum number of samples to split
        # 'min_samples_leaf':[1,3,5,7,9],     #the minimum number of samples to form a leaf
        # 'max_features':[2,3,4,5,6,7],     #square root of features is usually a good starting point
        # 'subsample':[0.7,0.75,0.8,0.85,0.9,0.95,1]}       #the fraction of samples to be used for fitting the individual base learners. Values lower than 1 generally lead to a reduction of variance and an increase in bias.## random search
        # random_search = model_selection.RandomizedSearchCV(model, 
        # param_distributions=param_dic, n_iter=1000, 
        # scoring="accuracy").fit(X_train, y_train)
        # print("Best Model parameters:", random_search.best_params_)
        # print("Best Model mean accuracy:", random_search.best_score_)
        # model = random_search.best_estimator_
        
        # Use statsmodels sm and smf to fit model
        formula = 'precip ~ ' + '+'.join([*X_names]) + '-1' # con categorica con intercepto
        print(formula)
        GLM_logistical = smf.glm(formula = formula,data=dtf_train, family=sm.families.Binomial())
        GLM_results = GLM_logistical.fit()
        print(GLM_results.summary())
        
    
        
        
    
    return GLM_results, dtf_train, dtf_test, dtf



if __name__ == '__main__':
    path = ['/','home','faarrosp','Documents','GitHub',
            'Demo-SRM','01_Maipo','01_RMELA']
    path = os.path.join(*path)
    print(path)
    GLM_results, dtf_train, dtf_test, dtf = classify_precipitation_dataframe(path)
    
    rainfall_train = GLM_results.predict(dtf_train)
    rainfall_train = rainfall_train.apply(will_it_rain)
    
    print(rainfall_train.sum()/dtf_train['precip'].sum())
    
    

