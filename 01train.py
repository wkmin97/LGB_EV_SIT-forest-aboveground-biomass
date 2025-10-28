# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 17:53:12 2024

@author: mwk
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:45:11 2023

@author: mwk
"""

from autogluon.tabular import TabularPredictor
import pandas as pd
from sklearn import model_selection

def tenfold_autoML(num_ev,drop_data):
    tenfold_train = pd.DataFrame()
    tenfold_test = pd.DataFrame()
    for i in range(1, 11):
        train_file_name = 'tenfold_data/' + 'train_data_' + str(i) + '.csv'
        train_data = pd.read_csv(train_file_name,header=0,index_col=None)
        train_id = train_data['id']
        
        train_data = train_data.drop(columns=['id',"Id","POINT_X","POINT_Y"])
        train_data = train_data.drop(columns=drop_label[drop_data])
        label = 'b1_agbd_19'
        print("Summary of class variable: \n", train_data[label].describe())
        save_path = 'AutogluonModels/' + str(drop_data) +'/EV' + str(num_ev)\
            + 'dorp_id' + str(drop_data) +'_model'
        # specifies folder to store trained models
        predictor = TabularPredictor(label=label, path=save_path).fit(train_data)
        
        test_file_name = 'tenfold_data/' + 'test_data_' + str(i) + '.csv'
        test_data = pd.read_csv(test_file_name,header=0,index_col=None)
        test_id = test_data['id']
        test_data = test_data.drop(columns=drop_label[drop_data])
        y_test = test_data[label]  # values to predict
        test_data = test_data.drop(columns=['id',"Id","POINT_X","POINT_Y"])
        test_data_nolab = test_data.drop(columns=[label])  
        # delete label column to prove we're not cheating
        test_data_nolab.head()
        predictor = TabularPredictor.load(save_path)  
        # unnecessary, just demonstrates how to load previously-trained 
        # predictor from file
        y_pred = predictor.predict(test_data_nolab)
        print("Predictions:  \n", y_pred)
        perf = predictor.evaluate_predictions(y_true=y_test, \
                                              y_pred=y_pred, auxiliary_metrics=True)
        predictor.leaderboard(test_data, silent=True)
        
        
        pre_train_NeuralNetFastAI = predictor.predict(train_data, model='NeuralNetFastAI')
        pre_train_LightGBMXT = predictor.predict(train_data, model='LightGBMXT')
        pre_train_LightGBM = predictor.predict(train_data, model='LightGBM')
        pre_train_CatBoost = predictor.predict(train_data, model='CatBoost')
        pre_train_WeightedEnsemble_L2 = predictor.predict(train_data, model='WeightedEnsemble_L2')
        pre_train_NeuralNetTorch = predictor.predict(train_data, model='NeuralNetTorch')
        pre_train_LightGBMLarge = predictor.predict(train_data, model='LightGBMLarge')
        pre_train_ExtraTreesMSE = predictor.predict(train_data, model='ExtraTreesMSE')
        pre_train_XGBoost = predictor.predict(train_data, model='XGBoost')
        pre_train_RandomForestMSE = predictor.predict(train_data, model='RandomForestMSE')
        pre_train_KNeighborsUnif = predictor.predict(train_data, model='KNeighborsUnif')
        pre_train_KNeighborsDist = predictor.predict(train_data, model='KNeighborsDist')
        pf_train = pd.DataFrame({'id':train_id,
                                 'biomass':train_data['b1_agbd_19'],
                                 'pre_train_NeuralNetFastAI':pre_train_NeuralNetFastAI,
                                 'pre_train_LightGBMXT':pre_train_LightGBMXT,
                                 'pre_train_LightGBM':pre_train_LightGBM,
                                 'pre_train_CatBoost':pre_train_CatBoost,
                                 'pre_train_WeightedEnsemble_L2':pre_train_WeightedEnsemble_L2,
                                 'pre_train_NeuralNetTorch':pre_train_NeuralNetTorch,
                                 'pre_train_LightGBMLarge':pre_train_LightGBMLarge,
                                 'pre_train_ExtraTreesMSE':pre_train_ExtraTreesMSE,
                                 'pre_train_XGBoost':pre_train_XGBoost,
                                 'pre_train_RandomForestMSE':pre_train_RandomForestMSE,
                                 'pre_train_KNeighborsUnif':pre_train_KNeighborsUnif,
                                 'pre_train_KNeighborsDist':pre_train_KNeighborsDist})
        tenfold_train = pd.concat([tenfold_train, pf_train], ignore_index=True)
        
        pre_test_NeuralNetFastAI = predictor.predict(test_data, model='NeuralNetFastAI')
        pre_test_LightGBMXT = predictor.predict(test_data, model='LightGBMXT')
        pre_test_LightGBM = predictor.predict(test_data, model='LightGBM')
        pre_test_CatBoost = predictor.predict(test_data, model='CatBoost')
        pre_test_WeightedEnsemble_L2 = predictor.predict(test_data, model='WeightedEnsemble_L2')
        pre_test_NeuralNetTorch = predictor.predict(test_data, model='NeuralNetTorch')
        pre_test_LightGBMLarge = predictor.predict(test_data, model='LightGBMLarge')
        pre_test_ExtraTreesMSE = predictor.predict(test_data, model='ExtraTreesMSE')
        pre_test_XGBoost = predictor.predict(test_data, model='XGBoost')
        pre_test_RandomForestMSE = predictor.predict(test_data, model='RandomForestMSE')
        pre_test_KNeighborsUnif = predictor.predict(test_data, model='KNeighborsUnif')
        pre_test_KNeighborsDist = predictor.predict(test_data, model='KNeighborsDist')
        pf_test = pd.DataFrame({ 'id':test_id,
                                 'biomass':test_data['b1_agbd_19'],
                                 'pre_test_NeuralNetFastAI':pre_test_NeuralNetFastAI,
                                 'pre_test_LightGBMXT':pre_test_LightGBMXT,
                                 'pre_test_LightGBM':pre_test_LightGBM,
                                 'pre_test_CatBoost':pre_test_CatBoost,
                                 'pre_test_WeightedEnsemble_L2':pre_test_WeightedEnsemble_L2,
                                 'pre_test_NeuralNetTorch':pre_test_NeuralNetTorch,
                                 'pre_test_LightGBMLarge':pre_test_LightGBMLarge,
                                 'pre_test_ExtraTreesMSE':pre_test_ExtraTreesMSE,
                                 'pre_test_XGBoost':pre_test_XGBoost,
                                 'pre_test_RandomForestMSE':pre_test_RandomForestMSE,
                                 'pre_test_KNeighborsUnif':pre_test_KNeighborsUnif,
                                 'pre_test_KNeighborsDist':pre_test_KNeighborsDist})
        tenfold_test = pd.concat([tenfold_test, pf_test], ignore_index=True)
    tenfold_train_file_name = 'tenfold_data/' + 'train_data_11model_drop'+ str(drop_data) + '.csv'
    # 将新的表格保存为文件
    tenfold_train.to_csv(tenfold_train_file_name)
    #my_model_name =  site_name + str(num_ev)
    #predictor.save(my_model_name)
    tenfold_test_file_name = 'tenfold_data/'  + 'test_data_11model_drop'+ str(drop_data) + '.csv'
    tenfold_test.to_csv(tenfold_test_file_name)
    return None

drop_label = [["ev","svc"],["ev"],["svc"],[]]
tenfold_autoML(2,0)
for drop_data in range(0, len(drop_label)):
    tenfold_autoML(2,drop_data)