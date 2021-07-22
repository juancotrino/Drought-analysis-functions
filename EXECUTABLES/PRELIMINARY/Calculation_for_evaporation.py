#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 23:31:16 2020

@author: juanmanuel
"""

from datetime import datetime, timedelta
from osgeo import gdal, gdal_array

raster_path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/evap/"

start = datetime.strptime("01-01-1981", "%d-%m-%Y")
end = datetime.strptime("31-12-2011", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))

    raster = raster_path + "Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + "_aligned.tif"
    #Open band 1 as array
    ds = gdal.Open(raster)
    arr = ds.GetRasterBand(1).ReadAsArray()
    
    #Calculation
    data1 = ((arr <= 0) * abs(arr))
    data2 = ((arr == -9999) * -9999)
    data3 = ((arr != -9999) * data1)
    data = data2 + data3
    
    #Save array, using ds as a prototype
    gdal_array.SaveArray(data.astype("float32"), raster, "GTIFF", ds)
    
    ds = None
    
    ds = gdal.Open(raster, 1)
    ds.GetRasterBand(1).SetNoDataValue(-9999)
    
    ds = None