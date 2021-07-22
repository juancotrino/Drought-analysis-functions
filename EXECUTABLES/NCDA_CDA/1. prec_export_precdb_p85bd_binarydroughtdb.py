#!/usr/bin/env python
# coding: utf-8

import numpy as np
import calendar
from scipy.signal import savgol_filter
from datetime import datetime, timedelta
from osgeo import gdal

start = datetime.strptime("01-01-2000", "%d-%m-%Y")
end = datetime.strptime("31-12-2005", "%d-%m-%Y")
analysis_period_years = end.year - start.year + 1
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

src_filepath = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/"

reference_raster = gdal.Open("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/P_CHIRPS.v2.0_mm-day-1_daily_1981.01.01_aligned.tif")
reference_raster_array = np.array(reference_raster.GetRasterBand(1).ReadAsArray())
raster_rows = len(reference_raster_array)
raster_columns = len(reference_raster_array[0])
reference_raster = None

#CODE FOR EXTRACT DATA FROM RASTERS. EXPORTED TO A DATABASE

db = np.zeros(shape=(raster_rows, raster_columns, analysis_period_years, 12, 31))



year = 0
month = 0
day = 0

for date in date_generated:
    fulldate = str(date.strftime("%Y.%m.%d"))
    raster = gdal.Open( src_filepath + "P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + "_aligned.tif" )
    raster_array = np.array(raster.GetRasterBand(1).ReadAsArray())
    raster = None
    db[:, :, year, month, day] = raster_array
    day += 1
    
    if date.year == (date + timedelta(days = 1)).year:
        if date.month != (date + timedelta(days = 1)).month:
            month += 1
            day = 0
    else:
        year += 1
        month = 0
        day = 0

np.save("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/prec_db.npy", db)
#-----------------------------------------------------------------------------------------------------------------

#CODE FOR CALCULATING MOTNHLY PERCENTILE 85. EXPORTED TO A DATABASE

db_month_p85 = np.empty((raster_rows, raster_columns, 12))

for row in range(raster_rows):
    for column in range(raster_columns):
        for month in range(12):
            a = np.array([])
            for year in range(analysis_period_years):
                days_of_month = calendar.monthrange(start.year + year, month + 1)[1]
                for day in range(days_of_month):
                    a = np.append(a, db[row, column, year, month, day])
            db_month_p85[row, column, month] = np.percentile(a, 15)

np.save("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/threshold_monthly_prec85.npy", db_month_p85)
#-----------------------------------------------------------------------------------------------------------------

#SETTING UP LEAP AND REGULAR YEARS

flat_p85_regular_year = np.empty((raster_rows, raster_columns, 365))
flat_p85_leap_year = np.empty((raster_rows, raster_columns, 366))

smooth_p85_regular_year = np.empty((raster_rows, raster_columns, 365))
smooth_p85_leap_year = np.empty((raster_rows, raster_columns, 366))

start_regular_year = datetime.strptime("01-01-1979", "%d-%m-%Y")#reference regular year
end_regular_year = datetime.strptime("31-12-1979", "%d-%m-%Y")
date_generated_regular_year = [start_regular_year + timedelta(days=x) for x in range(0, (end_regular_year-start_regular_year).days + 1)]

start_leap_year = datetime.strptime("01-01-1980", "%d-%m-%Y")#reference leap year
end_leap_year = datetime.strptime("31-12-1980", "%d-%m-%Y")
date_generated_leap_year = [start_leap_year + timedelta(days=x) for x in range(0, (end_leap_year-start_leap_year).days + 1)]
#-----------------------------------------------------------------------------------------------------------------

#CODE FOR GENERATING THRESHOLD SERIES FOR LEAP AND REGULAR YEARS

i = 0
j = 0
for row in range(raster_rows):
    for column in range(raster_columns):
        for date in date_generated_regular_year:
            flat_p85_regular_year[row, column, i] = db_month_p85[row, column, date.month - 1]
            i += 1
        for date in date_generated_leap_year:
            flat_p85_leap_year[row, column, j] = db_month_p85[row, column, date.month - 1]
            j += 1
        i = 0
        j = 0

np.save("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/flattened_threshold_monthly_p85_regular_year.npy", flat_p85_regular_year)
np.save("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/flattened_threshold_monthly_p85_leap_year.npy", flat_p85_leap_year)
#-----------------------------------------------------------------------------------------------------------------

#CODE FOR SMOOTHING THRESHOLDS FROM LEAP AND REGULAR YEARS

for row in range(raster_rows):
    for column in range(raster_columns):
        y_p85_regular_year = flat_p85_regular_year[row, column, :]
        y_p85_leap_year = flat_p85_leap_year[row, column, :]
        smooth_p85_regular_year[row, column, :] = savgol_filter(y_p85_regular_year, 45, 3) # window size 51, polynomial order 3
        smooth_p85_leap_year[row, column, :] = savgol_filter(y_p85_leap_year, 45, 3) # window size 51, polynomial order 3

np.save("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/smoothed_threshold_monthly_p85_regular_year.npy", smooth_p85_regular_year)
np.save("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/smoothed_threshold_monthly_p85_leap_year.npy", smooth_p85_leap_year)
#-----------------------------------------------------------------------------------------------------------------

#CODE FOR CALCULATING BINARY REPRESENTATION OF DROUGHT ACCORDING TO THE 85 PERCENTILE OF THE CODE ABOVE. EXPORTED TO A DATABASE

drought_binary_db = np.zeros(shape=(raster_rows, raster_columns, analysis_period_years, 12, 31)).astype('int')

for row in range(raster_rows):
    for column in range(raster_columns):
        for month in range(12):
            for year in range(analysis_period_years):
                days_of_month = calendar.monthrange(start.year + year, month + 1)[1]
                for day in range(days_of_month):
                    if db[row, column, year, month, day] == -9999:
                            drought_binary_db[row, column, year, month, day] = -9999
                    else:
                        if calendar.isleap(start.year + year):
                            if (db[row, column, year, month, day] - smooth_p85_leap_year[row, column, month]) >= 0:
                                drought_binary_db[row, column, year, month, day] = 0
                            else:
                                drought_binary_db[row, column, year, month, day] = 1
                        else:
                            if (db[row, column, year, month, day] - smooth_p85_regular_year[row, column, month]) >= 0:
                                drought_binary_db[row, column, year, month, day] = 0
                            else:
                                drought_binary_db[row, column, year, month, day] = 1

np.save("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/DBs/drought_binary_db.npy", drought_binary_db)
#-----------------------------------------------------------------------------------------------------------------

db = None
db_month_p85 = None
flat_p85_regular_year = None
flat_p85_leap_year = None
smooth_p85_regular_year = None
smooth_p85_leap_year = None
drought_binary_db = None