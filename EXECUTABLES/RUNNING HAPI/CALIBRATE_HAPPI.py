# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 22:13:37 2021

@author: juan.cotrino
"""

"""
This code is used to calibrate the model

-   you have to make the root directory to the examples folder to enable the code
    from reading input files

"""
#%links
from IPython import get_ipython   # to reset the variable explorer each time
get_ipython().magic('reset -f')
import os
os.chdir("C:/Users/juan.cotrino/Documents/JC_FA_TESIS/")

#%library
import numpy as np
import pandas as pd
from osgeo import gdal
# functions HAPI 0.2.0
from Hapi.calibration import RunCalibration
import Hapi.HBV as HBV
import Hapi.giscatchment as GC
import Hapi.distparameters as DP
import Hapi.performancecriteria as PC
#%%

PrecPath = prec_path="Datos/meteodata/calib/prec"
Evap_Path = evap_path="Datos/meteodata/calib/evap"
TempPath = temp_path="Datos/meteodata/calib/temp"
#DemPath = path+"GIS/4000/dem4000.tif"
FlowAccPath = "Datos/GIS/Mapa_General/RASTERS_CUENCA/flow_acc.tif"
FlowDPath = "Datos/GIS/Mapa_General/RASTERS_CUENCA/flow_dir.tif"
#%%

Paths=[PrecPath, Evap_Path, TempPath, FlowAccPath, FlowDPath, ]

###  Boundaries, p2
#p2[0]: Hours of time step
#p2[1]: Catchment area in km2
p2=[24, 270849.418285]
#[sp,sm,uz,lz,wc]
init_st=[0,250,70,70,0]
snow=0
UB=np.loadtxt("Datos/Calibration/UB.txt", usecols=0)
LB=np.loadtxt("Datos/Calibration/LB.txt", usecols=0)

Basic_inputs=dict(p2=p2, init_st=init_st, UB=UB, LB=LB, snow=snow)

### spatial variability function
"""
define how generated parameters are going to be distributed spatially
totaly distributed or totally distributed with some parameters are lumped
for the whole catchment or HRUs or HRUs with some lumped parameters
for muskingum parameters k & x include the upper and lower bound in both
UB & LB with the order of Klb then kub
function inside the calibration algorithm is written as following
par_dist=SpatialVarFun(par,*SpatialVarArgs,kub=kub,klb=klb)

"""
SpatialVarFun=DP.par3dLumped
raster=gdal.Open(FlowAccPath)
no_parameters=12
lumpedParNo=0
lumped_par_pos=[]
SpatialVarArgs=[raster,no_parameters]#,lumpedParNo,lumped_par_pos]

### Objective function
# stations discharge
Sdate='2000-01-01'
Edate='2012-12-31'
Qobs = pd.read_excel("Datos/Calibration/Discharge/Qobs_IDEAM.xlsx",sheet_name="Sheet1",convert_float=True, index_col=0)

Qobs.index = pd.to_datetime(Qobs.index)
Qobs.columns = Qobs.columns.map(unicode)
Qobs = Qobs.loc[Sdate:Edate]
Qobs_np=Qobs.to_numpy()

stations=pd.read_excel("Datos/Calibration/Discharge/Qobs_IDEAM.xlsx",sheet_name="coordinates",convert_float=True)
coordinates=stations[['id','x','y','weight']][:]

# calculate the nearest cell to each station
coordinates.loc[:,["cell_row","cell_col"]]=GC.NearestCell(raster,coordinates)
coordinates = coordinates.set_index('id')
coordinates.index = coordinates.index.map(unicode)

acc=gdal.Open(FlowAccPath )
acc_A=acc.ReadAsArray()
# define the objective function and its arguments
OF_args=[coordinates]

"""
OF is the objective function used for the calibration
OF function locates each station and extract the UZ and LZ discharge for each
station and sum both then calculate the error based on RMSE and gives a weight
for each station (weights are given in the excel sheet read in
the variable stations)

"""
def OF(Qobs,Qout,q_uz_routed,q_lz_trans,coordinates):
    
    all_errors=[]
    for station_id in Qobs:
    
        Quz = np.reshape(q_uz_routed[int(coordinates.loc[station_id, "cell_row"]),int(coordinates.loc[station_id, "cell_col"]),:-1],len(Qobs))
        Qlz = np.reshape(q_lz_trans[int(coordinates.loc[station_id, "cell_row"]),int(coordinates.loc[station_id, "cell_col"]),:-1],len(Qobs))
        Q = Quz + Qlz
        
        #CREATE DATAFRAME WITH AVAILABLE QOBS DATA AND DATE INDEXING
        Qobs_inner_station = pd.notnull(Qobs[station_id])
        dates_Qobs_avail = Qobs[Qobs_inner_station].index.tolist()
        Qobs_avail_df = Qobs.loc[dates_Qobs_avail,str(station_id)].to_frame()
        
        #CREATE DATAFRAME WITH CALCULATED Q AND DATE INDEXING
        Qcal_df = pd.DataFrame(Q, columns=["Qcal"], index=pd.date_range(start=Sdate, end=Edate))
        
        #MERGE BOTH TO COMPARE Q ONLY IN THE DATES GIVEN BY THE AVAILABLE DATA
        Q_compared = pd.merge(left=Qobs_avail_df, left_index=True, right=Qcal_df, right_index=True, how='inner')
        all_errors.append((PC.RMSE(Q_compared.loc[:,station_id].values,Q_compared.loc[:,'Qcal'].values))*coordinates.loc[station_id,'weight']) 
    
    print(all_errors)
    error = np.nansum(all_errors)
    return error

### Optimization
store_history=1
history_fname="Datos/Calibration/par_history.txt"
OptimizationArgs=[store_history,history_fname]
#%%
# run calibration
cal_parameters=RunCalibration(HBV, Paths, Basic_inputs,
                              SpatialVarFun, SpatialVarArgs,
                              OF,OF_args,Qobs,
                              OptimizationArgs,
                              printError=1)
#%% convert parameters to rasters
par=cal_parameters[1][:12]
klb=0.5
kub=1
Path="Datos/Calibration/Parameters/"

DP.SaveParameters(SpatialVarFun, raster, par, no_parameters,lumpedParNo, lumped_par_pos,snow ,kub, klb,Path)
