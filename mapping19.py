# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 22:01:12 2024

@author: mwk
"""

from autogluon.tabular import TabularPredictor
from osgeo import gdal
import os
import numpy as np
import rasterio
import pandas as pd


DEM_path = r"G:\project\USA_west\DEM"
LAI_path = r"G:\project\USA_west\LAI"
P2_path = r"G:\project\USA_west\palsar-2"
S1_path = r"G:\sentinel-1\S1_US"
S2_path = r"G:\sentinel-2"
nlcd_path = r"G:\project\USA_west\nlcd"
map_path = r"G:\project\USA_west\mapping"
in_dem_metrics = ["dem","slope"]
in_lai_metrics = ["LAI_2019_max","LAI_2019_mean","LAI_2019_min"]
in_p2_metrics = ["PALSAR2_HH","PALSAR2_HV"]
in_s1_metrics = ["S1_VH","S1_VV","S1_VV--VH"]
in_s2_metrics = ["B10","B11","B12","B2","B3","B4","B5","B6","B7","B8","B8A",
                 "EVI","EVI2","MSI","NDVI_B5","NDVI_B6","NDVI_B7","NDVI_B8",
                 "NDVI_B8A","RVI","SAVI","TCB","TCG","TCW"]
in_nlcd_metrics = ["tcc_19","landcover_19",'fch']
year='2019'

parameters = []
print('metrics preparating')
for dem_metrics in in_dem_metrics:
    dem_metrics_file = 'US_'+dem_metrics +'.tif'
    dem_sitePath = os.path.join(DEM_path,dem_metrics_file)
    with rasterio.open(dem_sitePath) as src:
        parameter = src.read(1)
        profile = src.profile   # 假设参数在第一个波段中
        parameters.append(parameter)

for lai_metrics in in_lai_metrics:
    lai_metrics_file = lai_metrics +'.tif'
    lai_sitePath = os.path.join(LAI_path,year,lai_metrics_file)
    with rasterio.open(lai_sitePath) as src:
        parameter = src.read(1)
        profile = src.profile   # 假设参数在第一个波段中
        parameters.append(parameter)
        
for p2_metrics in in_p2_metrics:
    p2_metrics_file = p2_metrics +'_19.tif'
    p2_sitePath = os.path.join(P2_path,p2_metrics_file)
    with rasterio.open(p2_sitePath) as src:
        parameter = src.read(1)
        profile = src.profile   # 假设参数在第一个波段中
        parameters.append(parameter)

for s1_metrics in in_s1_metrics:
    s1_metrics_file = s1_metrics +'_'+year+'.tif'
    s1_sitePath = os.path.join(S1_path,s1_metrics_file)
    with rasterio.open(s1_sitePath) as src:
        parameter = src.read(1)
        profile = src.profile   # 假设参数在第一个波段中
        parameters.append(parameter)

for s2_metrics in in_s2_metrics:
    s2_metrics_file = s2_metrics +'.tif'
    s2_sitePath = os.path.join(S2_path,year,s2_metrics_file)
    with rasterio.open(s2_sitePath) as src:
        parameter = src.read(1)
        profile = src.profile   # 假设参数在第一个波段中
        parameters.append(parameter)


for nlcd_metrics in in_nlcd_metrics:
    nlcd_metrics_file = nlcd_metrics +'.tif'
    nlcd_sitePath = os.path.join(nlcd_path,nlcd_metrics_file)
    with rasterio.open(nlcd_sitePath) as src:
        parameter = src.read(1)
        profile = src.profile   # 假设参数在第一个波段中
        parameters.append(parameter)

print('metrics preparated')


mapping = np.empty((1968, 2527), parameter.dtype)
model_path= 'AutogluonModels/0/EV2dorp_id0_model'
predictor = TabularPredictor.load(model_path)

columns_name = ["dem","slope","LAI_2019_max","LAI_2019_mean","LAI_2019_min",
                "PALSAR.2_HH_19","PALSAR.2_HV_19","s1_vh","s1_vv","s1_vvvh",
                "B10","B11","B12","B2","B3","B4","B5","B6","B7","B8","B8A",
                "EVI","EVI2","MSI","NDVI_B5","NDVI_B6","NDVI_B7","NDVI_B8",
                "NDVI_B8A","RVI","SAVI","TCB","TCG","TCW","tcc_19","landcover",
                "fch"]
map_data = pd.DataFrame(columns=columns_name, index=range(0,mapping.shape[1]), dtype=np.float32)

print('start mapping')
for row in range(0,mapping.shape[0]):
    print('start mapping row:',row)
    for col in range(0,mapping.shape[1]):
        for i in range(0,map_data.shape[1]):
            map_data.iloc[col,i] = parameters[i][row,col]
    map_data = map_data.fillna(0)
    predicted_value = predictor.predict(map_data)
    mapping[row, ] = predicted_value
    


print('mapping completed')
map_fileName = year + '.tif'
with rasterio.open(map_fileName, 'w', **profile) as dst:
    dst.write(mapping, 1)

map_fileName = year + '.csv'
mapping_csv = pd.DataFrame(mapping)
mapping_csv.to_csv(map_fileName)