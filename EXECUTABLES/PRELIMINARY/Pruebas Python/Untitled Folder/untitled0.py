# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 09:23:29 2019

@author: jmcotrino
"""

#import os
from osgeo import gdal
from datetime import datetime, timedelta
import time, sys
from netCDF4 import Dataset, date2num, num2date
import numpy as np


start = datetime.strptime("02-01-1979", "%d-%m-%Y")
end = datetime.strptime("05-01-1979", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

#Exports each band in separates archives
i = 1

#ds = "Downloads_ERAINTERIM/precipitation/1979-01-01_to_1979-06-01_precipitation.nc"
#do = "Downloads_ERAINTERIM/precipitation/NETCDF_files/MID/prec_" + str(date.strftime("%Y%m%d")) + ".nc"
#os.system("gdal_translate -b 1 -b 2 " + ds + " " + do)
#ds = None
#os.system("gdal_translate -of netCDF -a_srs EPSG:21897 daily-tp_" + str(date.strftime("%Y%m%d")) + ".nc Output_FileName_1.tif")
for date in date_generated:
    ds = gdal.Open("Downloads_ERAINTERIM/precipitation/1979-01-01_to_1979-06-01_precipitation.nc")
    do = "Downloads_ERAINTERIM/precipitation/NETCDF_files/MID/prec_" + str(date.strftime("%Y%m%d")) + ".nc"
#    os.system("gdal_translate -of NETCDF -b " + str(i) + " -b " + str(i + 1) + " " + ds + " " + do)
#    ds = gdal.Open("Downloads_ERAINTERIM/precipitation/1979-01-01_to_1979-06-01_precipitation.nc")
#    do = "Downloads_ERAINTERIM/precipitation/NETCDF_files/MID/prec_" + str(date.strftime("%Y%m%d")) + ".nc"
#    ds = os.system("gdal_translate -of netCDF -a_srs EPSG:21897 -b " + str(i) + ", " + str(i + 1) + " " + str(ds) + " " + str(do))
    #translate_options = gdal.TranslateOptions(bandList=[i, i + 1], format = 'Gtiff')
    translate_options = gdal.TranslateOptions(bandList=[i, i + 1], format = 'netCDF')
    ds = gdal.Translate(do, ds, options = translate_options)
    ds = None
    
#    ds = gdal.Open("Downloads_ERAINTERIM/precipitation/1979-01-01_to_1979-06-01_precipitation.nc")
#    translate_options = gdal.TranslateOptions(bandList=[i + 1], format = 'Gtiff')
#    ds = gdal.Translate("Downloads_ERAINTERIM/precipitation/NETCDF_files/MID/prec_" + str(date.strftime("%Y%m%d")) + "_1.tif", ds, options = translate_options)

    
    
#    #gdal.Translate("Downloads_ERAINTERIM/precipitation/NETCDF_files/MID/prec_" + str(date.strftime("%Y%m%d")) + ".nc","Downloads_ERAINTERIM/precipitation/1979-01-01_to_1979-06-01_precipitation.nc", bandList=[i, i + 1])
    i += 2
    
for date in date_generated:
    day = int(date.strftime("%Y%m%d"))
    f_in = 'Downloads_ERAINTERIM/precipitation/NETCDF_files/MID/prec_%d.nc' % day
    f_out = 'Downloads_ERAINTERIM/precipitation/NETCDF_files/TOTAL/daily-prec_%d.nc' % day
     
    d = datetime.strptime(str(day), '%Y%m%d')
    time_needed = [d + timedelta(hours = 12), d + timedelta(days = 1)]
     
    with Dataset(f_in) as ds_src:
        var_time = ds_src.variables['time']
        time_avail = num2date(var_time[:], var_time.units,
                calendar = var_time.calendar)
     
        indices = []
        for tm in time_needed:
            a = np.where(time_avail == tm)[0]
            if len(a) == 0:
                sys.stderr.write('Error: precipitation data is missing/incomplete - %s!\n'
                        % tm.strftime('%Y%m%d %H:%M:%S'))
                sys.exit(200)
            else:
                print('Found %s' % tm.strftime('%Y%m%d %H:%M:%S'))
                indices.append(a[0])
     
        var_tp = ds_src.variables['tp']
        tp_values_set = False
        for idx in indices:
            if not tp_values_set:
                data = var_tp[idx, :, :]
                tp_values_set = True
            else:
                data += var_tp[idx, :, :]
             
        with Dataset(f_out, mode = 'w', format = 'NETCDF3_64BIT_OFFSET') as ds_dest:
            # Dimensions
            for name in ['latitude', 'longitude']:
                dim_src = ds_src.dimensions[name]
                ds_dest.createDimension(name, dim_src.size)
                var_src = ds_src.variables[name]
                var_dest = ds_dest.createVariable(name, var_src.datatype, (name,))
                var_dest[:] = var_src[:]
                var_dest.setncattr('units', var_src.units)
                var_dest.setncattr('long_name', var_src.long_name)
     
            ds_dest.createDimension('time', None)
     
            # Variables
            var = ds_dest.createVariable('time', np.int32, ('time',))
            time_units = 'hours since 1900-01-01 00:00:00'
            time_cal = 'gregorian'
            var[:] = date2num([d], units = time_units, calendar = time_cal)
            var.setncattr('units', time_units)
            var.setncattr('long_name', 'time')
            var.setncattr('calendar', time_cal)
            var = ds_dest.createVariable(var_tp.name, np.double, var_tp.dimensions)
            var[0, :, :] = data
            var.setncattr('units', var_tp.units)
            var.setncattr('long_name', var_tp.long_name)
     
            # Attributes
            ds_dest.setncattr('Conventions', 'CF-1.6')
            ds_dest.setncattr('history', '%s %s'
                    % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    ' '.join(time.tzname)))
     
            print('Done! Daily total precipitation saved in %s' % f_out)
    

#os.system("gdal_translate -a_srs -b 1,2 EPSG:21897 Downloads_ERAINTERIM/precipitation/1979-01-01_to_1979-06-01_precipitation.nc TIFF_OUT.tif")

#Calculates the total daily precipitation
#for date in date_generated:
    
    #os.system("gdal_translate -of netCDF -a_srs EPSG:21897 daily-tp_" + str(date.strftime("%Y%m%d")) + ".nc Output_FileName_1.tif")
    #os.system("gdal_translate -a_srs -b 1,2 EPSG:21897 Downloads_ERAINTERIM/precipitation/1979-01-01_to_1979-06-01_precipitation.nc")