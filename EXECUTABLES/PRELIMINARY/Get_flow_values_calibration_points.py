#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 22:27:24 2020

@author: juanmanuel
"""

from osgeo import gdal, ogr
from datetime import datetime, timedelta
import pandas as pd


start = datetime.strptime("01-01-2000", "%d-%m-%Y")
end = datetime.strptime("31-12-2015", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

shp_filename = 'E:/Tesis//Datos/GIS/CALIBRATION_POINTS/CALIBRATION_POINTS.shp'
path = 'E:/Tesis/Datos/meteodata/calib/flow/'
excel_path = 'E:/Tesis/Datos/DBs/'

ds=ogr.Open(shp_filename)
lyr=ds.GetLayer()

features = ['Fecha']

for feat in lyr:
    features.append(str(feat.GetField('id')))

df = pd.DataFrame(columns=features)

i=0

for date in date_generated:
    fulldate = int(date.strftime("%Y%m%d"))
    src_filename = path + "daily-flow_" + str(fulldate) + ".tif"
    src_ds=gdal.Open(src_filename)
    gt=src_ds.GetGeoTransform()
    rb=src_ds.GetRasterBand(1)
    
    df.at[i, 'Fecha'] = date.strftime('%d/%m/%Y')
    
    ds=ogr.Open(shp_filename)
    lyr=ds.GetLayer()
    
    for feat in lyr:
        
        geom = feat.GetGeometryRef()
        feat_id = feat.GetField('id')
        mx, my = geom.GetX(), geom.GetY()  #coord in map units
        #Convert from map to pixel coordinates.
        #Only works for geotransforms with no rotation.
        px = int((mx - gt[0]) / gt[1]) #x pixel
        py = int((my - gt[3]) / gt[5]) #y pixel
        intval = rb.ReadAsArray(px, py, 1, 1)
        df.at[i, str(feat_id)] = intval[0][0]

    i+=1

df.to_excel(excel_path + 'Qobs.xlsx', index = False)