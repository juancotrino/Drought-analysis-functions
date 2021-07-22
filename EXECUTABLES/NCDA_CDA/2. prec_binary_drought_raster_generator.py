#!/usr/bin/env python
# coding: utf-8

import numpy as np
from datetime import datetime, timedelta
from osgeo import gdal, gdal_array

start = datetime.strptime("01-01-1981", "%d-%m-%Y")
end = datetime.strptime("31-12-1985", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

dst_filepath = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/NCDA_CDA/Drought_binary_TIFF/prec/"
drought_binary_db = np.load("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/drought_binary_db.npy")
reference_raster = gdal.Open("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/P_CHIRPS.v2.0_mm-day-1_daily_1981.01.01_aligned.tif")

#CODE FOR GENERATING RASTERS WITH BINARY REPRESENTATION OF DROUGHT ACCORDING TO THE SMOOTHED 85 PERCENTILE

for date in date_generated:

    fulldate = str(date.strftime("%Y.%m.%d"))
    dst_filename = dst_filepath + "P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + ".tif"

    gdal_array.SaveArray(drought_binary_db[:, :, (date.year - start.year), date.month - 1, date.day - 1], dst_filename, format = "GTIFF", prototype = reference_raster)
    
    ds = gdal.Open(dst_filename, 1)
    ds.GetRasterBand(1).SetNoDataValue(-9999)
    
    ds = None
#-----------------------------------------------------------------------------------------------------------------

drought_binary_db = None
reference_raster = None