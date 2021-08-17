# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 21:46:16 2020

@author: juan.cotrino
"""

variable = 'prec'

main_path = "E:/JC_FA_TESIS/"

start_date = "01-01-2000"
end_date = "31-12-2015"

src_filepath = main_path + "Datos/meteodata/total/" + variable + "/"
file_first_str = "_P_CHIRPS.v2.0_mm-day-1_daily_"
file_second_str = "_aligned.tif" 
date_format = "%Y.%m.%d"
output_path = main_path + "Datos/DBs/" + variable + "/"

import pickle
import numpy as np
import pandas as pd
from scipy.stats import gamma, norm
from scipy.signal import savgol_filter
from skimage.morphology import remove_small_objects
import calendar
from datetime import datetime, timedelta
from osgeo import gdal
import cv2

from Hapi.raster import RasterLike


def RastersToDataBase(start_date, end_date, variable, src_filepath,
                      file_first_str, file_second_str,date_format, output_path):
    
    start = datetime.strptime(start_date, "%d-%m-%Y")
    end = datetime.strptime(end_date, "%d-%m-%Y")
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
                    
    db_daily = {}
    db_daily['start'] = start
    db_daily['end'] = end
    
    db_monthly = {}
    db_monthly['start'] = start
    db_monthly['end'] = end

    first_date = str(start.strftime(date_format))
    raster = gdal.Open( src_filepath + str(0) + file_first_str + first_date + file_second_str )
    raster_array = np.array(raster.GetRasterBand(1).ReadAsArray())
    raster = None
    no_rows = raster_array.shape[0]
    no_columns = raster_array.shape[1]
    
    db_daily['data'] = np.empty((no_rows, no_columns, len(date_generated)))
    no_months = end.month - start.month + 12*(end.year - start.year) + 1
    db_monthly['data'] = np.empty((no_rows, no_columns, no_months))
    acc_daily = np.full((no_rows, no_columns), 0).astype(np.float64)
    
    i = 0
    m = 0
    for date in date_generated:
        fulldate = str(date.strftime(date_format))
        raster = gdal.Open( src_filepath + str(i) + file_first_str + fulldate + file_second_str )
        raster_array = np.array(raster.GetRasterBand(1).ReadAsArray())
        raster = None
        db_daily['data'][:, :, i] = raster_array
        if date.month == (date + timedelta(days=1)).month:
            acc_daily += raster_array
        else:
            acc_daily += raster_array
            db_monthly['data'][:, :, m] = acc_daily #/ date.day
            acc_daily = np.full((no_rows, no_columns), 0).astype(np.float64)
            m += 1
        
        i += 1
            
    output_files = [output_path + variable + "_daily_db.pickle",
                    output_path + variable + "_monthly_db.pickle"]
    
    dbs = [db_daily, db_monthly]
    
    for output_file, db in zip(output_files, dbs):
        with open(output_file, 'wb') as handle:
            pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)


RastersToDataBase(start_date,
                  end_date, 
                  variable,
                  src_filepath, 
                  file_first_str, 
                  file_second_str, 
                  date_format, 
                  output_path)
