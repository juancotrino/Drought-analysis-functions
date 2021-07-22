# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 19:15:10 2020

@author: juan.cotrino-p
"""

#%library
import gdal
from datetime import datetime, timedelta
import time

# HAPI modules
from Hapi.run import RunHapi
import Hapi.hbv as HBV
import Hapi.raster as GIS
#%%
"""
paths to meteorological data
"""

main_path = "C:/Users/juan.cotrino/Documents/JC_FA_TESIS/"
PrecPath = main_path + "Datos/meteodata/total/prec"
Evap_Path = main_path + "Datos/meteodata/total/evap"
TempPath = main_path + "Datos/meteodata/total/temp"
FlowAccPath = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/flow_acc.tif"
FlowDPath = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/flow_dir.tif"
ParPathRun = main_path + "Datos/Calibration/Parameters"
Paths = [PrecPath, Evap_Path, TempPath, FlowAccPath, FlowDPath, ]
p2=[24, 270849.418285]
init_st=[0,250,70,70,0]
snow=0

print('Model starts', time.ctime())
st, q_out, q_uz_routed, q_lz_trans = RunHapi(HBV,Paths,ParPathRun,p2,init_st,snow)
print('Model ends', time.ctime())

# %% store the result into rasters

src=gdal.Open(FlowAccPath)
start_date = "01-01-2000"
end_date = "31-12-2015"

variables = ['runoff', 'soil_moisture']
q_total = q_uz_routed + q_lz_trans
sm = st[:,:,:,1]

for variable in variables:
    # create list of names
    start = datetime.strptime(start_date, "%d-%m-%Y")
    end = datetime.strptime(end_date, "%d-%m-%Y")
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    resultspath = main_path + "Datos/model_results/" + variable + "/" + variable + "_"
    names=[resultspath + str(i)[:-9] for i in date_generated]
    names=[i.replace("-","_") for i in names]
    names=[i+".tif" for i in names]
    
    """
    to save the upper zone discharge distributerd discharge in a raster forms
    uncomment the next line
    """
    if variable == 'runoff':
        GIS.RastersLike(src,q_total[:,:,:-1],names)
    if variable == 'soil_moisture':
        GIS.RastersLike(src,sm[:,:,:-1],names)

src = None
print('\a')
