# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 15:41:30 2020

@author: jmcotrino
"""

from datetime import datetime, timedelta
from osgeo import gdal, gdal_array
#import os

start = datetime.strptime("01-01-1979", "%d-%m-%Y")
end = datetime.strptime("31-12-2011", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

#Set files path
src_filepath = "/Users/juanmanuel/Documents/OneDrive - ESCUELA COLOMBIANA DE INGENIERIA JULIO GARAVITO/1. TRABAJO DE GRADO/1. Tesis/2. Datos/0. Datos 20190912/Datos _iniciales/data/Downloads_ERAINTERIM/precipitation/TIFF_files/TOTAL_daily/"
dst_filepath = "/Users/juanmanuel/Desktop/MONTH/prec/"
shpfile_clip = '/Users/juanmanuel/Documents/OneDrive - ESCUELA COLOMBIANA DE INGENIERIA JULIO GARAVITO/1. TRABAJO DE GRADO/1. Tesis/2. Datos/0. Datos 20190912/Datos _iniciales/data/GIS/Mapa_General/cuenca_magdalena_proyectado.shp'

i = 0

for date in date_generated:
    
    fulldate = int(date.strftime("%Y%m%d"))
    
    #Open existing dataset
    src_ds_A = gdal.Open( src_filepath + "daily-prec_" + str(fulldate) + ".tiff" )

    if i == 0:
        # Open band 1 as array
        b1_A = src_ds_A.GetRasterBand(1)
        arr_A = b1_A.ReadAsArray() * 1000 #Multiplying by 1000 to convert it to mm
        data = arr_A
        i += 1
        continue
    else:
        src_ds_B = gdal.Open( src_filepath + "daily-prec_" + str(fulldate) + ".tiff" )
        b1_B = src_ds_B.GetRasterBand(1)
        arr_B = b1_B.ReadAsArray() * 1000 #Multiplying by 1000 to convert it to mm
        data = data + arr_B
        date_month = int(date.strftime("%Y%m"))
        i += 1
        if (date + timedelta(days = 1)).day == 1 or date_generated.index(date) == len(date_generated) - 1:
            #Set output
            dst_ds = dst_filepath + "monthly-prec_" + str(date_month) + ".tiff"
            gdal_array.SaveArray(data.astype("float64"), dst_ds, format = "GTIFF", prototype = src_ds_A)
            gdal.Warp(dst_ds, 
                      dst_ds, 
                      srcSRS='EPSG:21897', 
                      dstSRS='EPSG:21897', 
                      cutlineDSName=shpfile_clip,
                      cropToCutline=True,
                      dstNodata=0)
            #Properly close the datasets to flush to disk
            src_ds_A = None
            src_ds_B = None
            i = 0