#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 05:40:41 2020

@author: juanmanuel
"""

from osgeo import gdal, ogr
from osgeo.gdalconst import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
gdal.PushErrorHandler('CPLQuietErrorHandler')

#The next functions were taken from https://gist.github.com/perrygeo/5667173

def bbox_to_pixel_offsets(gt, bbox):
    originX = gt[0]
    originY = gt[3]
    pixel_width = gt[1]
    pixel_height = gt[5]
    x1 = int((bbox[0] - originX) / pixel_width)
    x2 = int((bbox[1] - originX) / pixel_width) + 1

    y1 = int((bbox[3] - originY) / pixel_height)
    y2 = int((bbox[2] - originY) / pixel_height) + 1

    xsize = x2 - x1
    ysize = y2 - y1
    return (x1, y1, xsize, ysize)


def zonal_stats(vector_path, raster_path, nodata_value=None, global_src_extent=False):
    rds = gdal.Open(raster_path, GA_ReadOnly)
    assert(rds)
    rb = rds.GetRasterBand(1)
    rgt = rds.GetGeoTransform()

    if nodata_value:
        nodata_value = float(nodata_value)
        rb.SetNoDataValue(nodata_value)

    vds = ogr.Open(vector_path, GA_ReadOnly)  # TODO maybe open update if we want to write stats
    assert(vds)
    vlyr = vds.GetLayer(0)

    # create an in-memory numpy array of the source raster data
    # covering the whole extent of the vector layer
    if global_src_extent:
        # use global source extent
        # useful only when disk IO or raster scanning inefficiencies are your limiting factor
        # advantage: reads raster data in one pass
        # disadvantage: large vector extents may have big memory requirements
        src_offset = bbox_to_pixel_offsets(rgt, vlyr.GetExtent())
        src_array = rb.ReadAsArray(*src_offset)

        # calculate new geotransform of the layer subset
        new_gt = (
            (rgt[0] + (src_offset[0] * rgt[1])),
            rgt[1],
            0.0,
            (rgt[3] + (src_offset[1] * rgt[5])),
            0.0,
            rgt[5]
        )

    mem_drv = ogr.GetDriverByName('Memory')
    driver = gdal.GetDriverByName('MEM')

    # Loop through vectors
    stats = []
    feat = vlyr.GetNextFeature()
    
    while feat is not None:

        if not global_src_extent:
            # use local source extent
            # fastest option when you have fast disks and well indexed raster (ie tiled Geotiff)
            # advantage: each feature uses the smallest raster chunk
            # disadvantage: lots of reads on the source raster
            src_offset = bbox_to_pixel_offsets(rgt, feat.geometry().GetEnvelope())
            src_array = rb.ReadAsArray(*src_offset)

            # calculate new geotransform of the feature subset
            new_gt = (
                (rgt[0] + (src_offset[0] * rgt[1])),
                rgt[1],
                0.0,
                (rgt[3] + (src_offset[1] * rgt[5])),
                0.0,
                rgt[5]
            )

        # Create a temporary vector layer in memory
        mem_ds = mem_drv.CreateDataSource('out')
        mem_layer = mem_ds.CreateLayer('poly', None, ogr.wkbPolygon)
        mem_layer.CreateFeature(feat.Clone())

        # Rasterize it
        rvds = driver.Create('', src_offset[2], src_offset[3], 1, gdal.GDT_Byte)
        rvds.SetGeoTransform(new_gt)
        gdal.RasterizeLayer(rvds, [1], mem_layer, burn_values=[1])
        rv_array = rvds.ReadAsArray()

        # Mask the source data array with our current feature
        # we take the logical_not to flip 0<->1 to get the correct mask effect
        # we also mask out nodata values explictly
        masked = np.ma.MaskedArray(
            src_array,
            mask=np.logical_or(
                src_array == nodata_value,
                np.logical_not(rv_array)
            )
        )

        feature_stats = {
            'min': float(masked.min()),
            'mean': float(masked.mean()),
            'max': float(masked.max()),
            'std': float(masked.std()),
            'sum': float(masked.sum()),
            'count': int(masked.count()),
            'fid': int(feat.GetFID())}

        stats.append(feature_stats)

        rvds = None
        mem_ds = None
        feat = vlyr.GetNextFeature()

    vds = None
    rds = None
    return stats

start = datetime.strptime("01-01-1981", "%d-%m-%Y")
end = datetime.strptime("31-12-2011", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

raster_path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/"
parameter_list = ['evap', 'prec', 'temp']
reservoirs = ['BETANIA', 'EL QUIMBO', 'SALVAJINA']

df = pd.DataFrame(columns=['date', 'plake', 'et', 't', 'tm', 'Q'])
df['date'] = date_generated

for reservoir in reservoirs:
    
    input_zone_polygon = '/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/GIS/EMBALSES_MAG_CAU/' + reservoir + '.shp'
    
    for parameter in parameter_list:
        
        data_list = []
        
        for date in date_generated:

            fulldate = str(date.strftime("%Y.%m.%d"))
            
            if parameter == "evap":
                raster_name = "/Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + "_aligned.tif"
            elif parameter == "prec":
                raster_name = "/P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + "_aligned.tif"
            elif parameter == "temp":
                raster_name = "/Tair2m_ECMWF_ERA-Interim_C_daily_" + fulldate + "_aligned.tif"
            
            raster = raster_path + parameter + raster_name
            
            data_list.append(zonal_stats(input_zone_polygon, raster)[0]['mean'])
            
        if parameter == "evap":
            df['et'] = data_list
        elif parameter == "prec":
            df['plake'] = data_list
        else:
            df['t'] = data_list

    df.to_csv("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/" + reservoir + ".csv", index=False)