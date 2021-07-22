#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:44:13 2020

@author: juanmanuel
"""

import os
import glob
from datetime import datetime, timedelta

prec_raster_path = "E:/JC_FA_TESIS/Datos/meteodata/calib/prec/"
evap_raster_path = "E:/JC_FA_TESIS/Datos/meteodata/calib/evap/"
temp_raster_path = "E:/JC_FA_TESIS/Datos/meteodata/calib/temp/"

tifCounter_prec = len(glob.glob1(prec_raster_path,"*.tif"))
tifCounter_evap = len(glob.glob1(evap_raster_path,"*.tif"))
tifCounter_temp = len(glob.glob1(temp_raster_path,"*.tif"))

start = datetime.strptime("01-01-1981", "%d-%m-%Y")
end = datetime.strptime("31-12-2011", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

i=0
os.chdir(prec_raster_path)
for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))
    #PRECIPITATION
    prec_file_name = str(i) + "_P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + "_aligned.tif"
    prec_output = os.rename(prec_file_name, "P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + "_aligned.tif")
    i+=1
    
i=0
os.chdir(evap_raster_path)
for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))
    #EVAPOTRANSPIRATION
    evap_file_name = str(i) + "_Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + "_aligned.tif"
    evap_output = os.rename(evap_file_name, "Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + "_aligned.tif")
    i+=1
    
i=0
os.chdir(temp_raster_path)
for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))
    #TEMPERATURE
    temp_file_name = str(i) + "_Tair2m_ECMWF_ERA-Interim_C_daily_" + fulldate + "_aligned.tif"
    temp_output = os.rename(temp_file_name, "Tair2m_ECMWF_ERA-Interim_C_daily_" + fulldate + "_aligned.tif")
    i+=1
    
i=0