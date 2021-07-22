#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:44:13 2020

@author: juanmanuel
"""

import os
from datetime import datetime, timedelta

prec_raster_path = "C:/Users/juan.cotrino/Documents/JC_FA_TESIS/Datos/meteodata/valid/prec/"
evap_raster_path = "C:/Users/juan.cotrino/Documents/JC_FA_TESIS/Datos/meteodata/valid/evap/"
temp_raster_path = "C:/Users/juan.cotrino/Documents/JC_FA_TESIS/Datos/meteodata/valid/temp/"

start = datetime.strptime("01-01-2012", "%d-%m-%Y")
end = datetime.strptime("31-12-2015", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

index = 4383

os.chdir(prec_raster_path)
for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))
    
    #PRECIPITATION
    prec_file_name = "P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + "_aligned.tif"
    prec_output = os.rename(prec_file_name, str(index) + "_" + prec_file_name)
    index += 1
index = 4383

os.chdir(evap_raster_path)
for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))
    
    #EVAPOTRANSPIRATION
    evap_file_name = "Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + "_aligned.tif"
    evap_output = os.rename(evap_file_name, str(index) + "_" + evap_file_name)
    index += 1
index = 4383

os.chdir(temp_raster_path)
for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))
    
    #TEMPERATURE
    temp_file_name = "Tair2m_ECMWF_ERA-Interim_C_daily_" + fulldate + "_aligned.tif"
    temp_output = os.rename(temp_file_name, str(index) + "_" + temp_file_name)
    index += 1
index = 0