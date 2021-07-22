#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 22:39:27 2020

@author: juanmanuel
"""

from osgeo import gdal
import numpy as np

DEMPath = "E:/JC_FA_TESIS/Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM_TEST.tif"

raster = gdal.Open(DEMPath, 1)
band = raster.GetRasterBand(1)

np_array = band.ReadAsArray()
new_np_array = np_array
changed_cells_array = np.zeros(np_array.shape)

inc_percentage = 1.01

NoDataValue = band.GetNoDataValue()

#%%
#===========================================BY ROWS===============================================
for i in range(np_array.shape[0]):
    for j in range(np_array.shape[1]):
        surr_cells_value = []
        
        if np_array[i, j] == NoDataValue:
            new_np_array[i, j] = np_array[i, j]
            changed_cells_array[i, j] = 0
            continue
        else:
            try:
                if np_array[i - 1, j - 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 1, j - 1])
            except:
                pass
            
            try:
                if np_array[i - 1, j - 0] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 1, j - 0])
            except:
                pass
            
            try:
                if np_array[i - 1, j + 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 1, j + 1])
            except:
                pass
            
            try:
                if np_array[i - 0, j - 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 0, j - 1])
            except:
                pass
            
            try:                
                if np_array[i - 0, j + 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 0, j + 1])
            except:
                pass
            
            try:                    
                if np_array[i + 1, j - 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i + 1, j - 1])
            except:
                pass
            
            try:                    
                if np_array[i + 1, j - 0] != NoDataValue:
                    surr_cells_value.append(new_np_array[i + 1, j - 0])
            except:
                pass
            
            try:                    
                if np_array[i + 1, j + 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i + 1, j + 1])
            except:
                pass
                        
            max_value = max(surr_cells_value)
            
#            if i == 174 and j == 51:
#                print("Pare acá")
            
            if len(surr_cells_value) == 8 or new_np_array[i, j] > max_value or new_np_array[i, j] > min(surr_cells_value):
                new_np_array[i, j] = np_array[i, j]
                changed_cells_array[i, j] = 0
            else:
                try:
                    if new_np_array[i, j] < min(surr_cells_value):
                        new_np_array[i, j] = min(surr_cells_value) * inc_percentage
                        changed_cells_array[i, j] = 1
                        continue
                except:
                    pass
#                new_np_array[i, j] = np_array[i, j] * inc_percentage
#                changed_cells_array[i, j] = 1
                    
            
#%%
#===========================================BY COLUMNS===============================================  
        
for j in range(np_array.shape[1]):
    for i in range(np_array.shape[0]):
        surr_cells_value = []
        
        if changed_cells_array[i, j] == 1:
            continue

        if np_array[i, j] == NoDataValue:
            new_np_array[i, j] = np_array[i, j]
            changed_cells_array[i, j] = 0
            continue
        else:
            try:
                if np_array[i - 1, j - 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 1, j - 1])
            except:
                pass
            
            try:
                if np_array[i - 1, j - 0] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 1, j - 0])
            except:
                pass
            
            try:
                if np_array[i - 1, j + 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 1, j + 1])
            except:
                pass
            
            try:
                if np_array[i - 0, j - 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 0, j - 1])
            except:
                pass
            
            try:                
                if np_array[i - 0, j + 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i - 0, j + 1])
            except:
                pass
            
            try:                    
                if np_array[i + 1, j - 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i + 1, j - 1])
            except:
                pass
            
            try:                    
                if np_array[i + 1, j - 0] != NoDataValue:
                    surr_cells_value.append(new_np_array[i + 1, j - 0])
            except:
                pass
            
            try:                    
                if np_array[i + 1, j + 1] != NoDataValue:
                    surr_cells_value.append(new_np_array[i + 1, j + 1])
            except:
                pass
                        
            max_value = max(surr_cells_value)
            
            if len(surr_cells_value) == 8 or new_np_array[i, j] > max_value or new_np_array[i, j] > min(surr_cells_value):
                new_np_array[i, j] = np_array[i, j]
                changed_cells_array[i, j] = 0
            else:
                try:
                    if new_np_array[i, j] < min(surr_cells_value):
                        new_np_array[i, j] = min(surr_cells_value) * inc_percentage
                        changed_cells_array[i, j] = 1
                        continue
                except:
                    pass
#                new_np_array[i, j] = np_array[i, j] * inc_percentage
#                changed_cells_array[i, j] = 1
        

#%%

#for i in range(np_array.shape[0]):
#    for j in range(np_array.shape[1]):
#        if new_np_array[i, j] == NoDataValue:
#            continue
#        if new_np_array[i, j] < 0:
#            new_np_array[i, j] = 0

band.WriteArray(new_np_array)

band = None 
raster = None
