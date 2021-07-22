#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 18:13:16 2020

@author: juanmanuel
"""

from datetime import datetime, timedelta
from Hapi import raster as GIS
from osgeo import gdal

dem_path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"
input_raster_path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/"
output_raster_path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/"

start = datetime.strptime("01-01-1981", "%d-%m-%Y")
end = datetime.strptime("31-12-2011", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

def align_parameter(dem, parameter_raster, output):
    
    DEM = gdal.Open(dem)
    raster = gdal.Open(parameter_raster)
    
    # align
    aligned_raster = GIS.MatchRasterAlignment(DEM, raster)
    dst_Aligned_M = GIS.MatchNoDataValue(DEM, aligned_raster)
    
    # save the new raster
    GIS.SaveRaster(dst_Aligned_M, output)
    
    DEM = None
    raster = None

for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))
    
    #PRECIPITATION
    
    prec_input = input_raster_path + "prec/CHIRPS/P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + ".tif"
    prec_output = output_raster_path + "prec/P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + "_aligned.tif"
    align_parameter(dem_path, prec_input, prec_output)
    
    #EVAPOTRANSPIRATION
    
    evap_input = input_raster_path + "evap/ERA_INTERIM/Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + ".tif"
    evap_output = output_raster_path + "evap/Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + "_aligned.tif"
    align_parameter(dem_path, evap_input, evap_output)
    
    #TEMPERATURE

    temp_input = input_raster_path + "temp/ERA_INTERIM/Tair2m_ECMWF_ERA-Interim_C_daily_" + fulldate + ".tif"
    temp_output = output_raster_path + "temp/Tair2m_ECMWF_ERA-Interim_C_daily_" + fulldate + "_aligned.tif"
    align_parameter(dem_path, temp_input, temp_output)