#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:21:39 2020

@author: juanmanuel
"""

import os
#os.system("gdalinfo")
#os.environ['CONDA_PREFIX']
#os.environ['GDAL_DATA'] = os.environ['CONDA_PREFIX'] + '/Library/share/gdal'

from zipfile import ZipFile
import cdsapi
import gdal
from datetime import datetime, timedelta
from Hapi import raster as GIS


dem_path = "E:/JC_FA_TESIS/Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"

start = datetime.strptime("01-01-2000", "%d-%m-%Y")
end = datetime.strptime("03-01-2000", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

path = 'E:/JC_FA_TESIS/Datos/meteodata/calib/'#flow/'
dst_filepath = path
dst_file = path + 'download.zip'

def align_parameter(dem, parameter_raster, output):
    
    DEM = gdal.Open(dem)
    raster = gdal.Open(parameter_raster)
    print('raster leido como: ', raster)
    # align
    aligned_raster = GIS.MatchRasterAlignment(DEM, raster)
    dst_Aligned_M = GIS.MatchNoDataValue(DEM, aligned_raster)
    
    # save the new raster
    GIS.SaveRaster(dst_Aligned_M, output)
    
    DEM = None
    raster = None

for date in date_generated:
    
    fulldate = int(date.strftime("%Y%m%d"))
    
    #DOWNLOAD DATA
    c = cdsapi.Client()

    c.retrieve(
        'cems-glofas-historical',
        {
            'variable': 'River discharge',
            'dataset': 'Consolidated reanalysis',
            'version': '2.1',
            "area"   : "11.1/-76.93/1.57/-72.2",
            'grid'    : '1.0/1.0',
            'year': date.strftime('%Y'),
            'month': date.strftime('%m'),
            'day': date.strftime('%d'),
            'format': 'zip',
        },
        dst_file)
    
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile(dst_file, 'r') as zipObj:
      # Extract all the contents of zip file in current directory
      zipObj.extractall(path)
    
    os.remove(dst_file)

    #Open existing dataset
    src_ds = gdal.Open( path + "CEMS_ECMWF_dis24_" + str(fulldate) + "_glofas_v2.1.nc" )
    
    #Open output format driver, see gdal_translate --formats for list
    format = "GTiff"
    driver = gdal.GetDriverByName( format )
    
#    GDAL_DATA=C:\Python35\Lib\site-packages\osgeo\data\gdal
    
    #Output to new format
    dst_ds = path + "daily-flow_" + str(fulldate) + ".tif"
    #Reproject to different coordinate system
    
    input_raster = path + "CEMS_ECMWF_dis24_" + str(fulldate) + "_glofas_v2.1.nc"
    output_raster = path + "daily-flow_" + str(fulldate) + "_aligned.tif"
    align_parameter(dem_path, input_raster, output_raster)
    
    # gdal.Warp(dst_ds, 
    #           src_ds, 
    #           srcSRS='EPSG:4326', 
    #           dstSRS='EPSG:21897', 
    #           cutlineDSName=shpfile_clip,
    #           cropToCutline=True,
    #           dstNodata=-9999)
    
    src_ds = None
    os.remove(path + "CEMS_ECMWF_dis24_" + str(fulldate) + "_glofas_v2.1.nc")