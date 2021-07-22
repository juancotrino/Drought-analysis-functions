# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 16:37:41 2020

@author: juanmanuel
"""

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
    raster = gdal.Open( src_filepath + file_first_str + first_date + file_second_str )
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
        raster = gdal.Open( src_filepath + file_first_str + fulldate + file_second_str )
        raster_array = np.array(raster.GetRasterBand(1).ReadAsArray())
        raster = None
        db_daily['data'][:, :, i] = raster_array
        if date.month == (date + timedelta(days=1)).month:
            acc_daily += raster_array
        else:
            acc_daily += raster_array
            db_monthly['data'][:, :, m] = acc_daily
            acc_daily = np.full((no_rows, no_columns), 0).astype(np.float64)
            m += 1
        
        i += 1
            
    output_files = [output_path + variable + "_daily_db.pickle",
                    output_path + variable + "_monthly_db.pickle"]
    
    dbs = [db_daily, db_monthly]
    
    for output_file, db in zip(output_files, dbs):
        with open(output_file, 'wb') as handle:
            pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    
def MonthlyPercentile(db_file, percentile, variable, output_path):
    """
    CODE FOR CALCULATING MOTNHLY GIVEN PERCENTILE. EXPORTED TO A DATABASE
    
    - start_date : "01-01-2000"
    - end_date : "31-12-2011"
    - db : [row, column, year, month, day]
    - percentile : 0 < perc < 100 (Inverse percentile)
    - src_filepath : "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/" (Absolute path)
    - reference_file : "0_P_CHIRPS.v2.0_mm-day-1_daily_2000.01.01_aligned.tif"
    """

    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
            
    start = db['start']
    end = db['end']
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

    no_rows = db['data'].shape[0]
    no_columns = db['data'].shape[1]
            
    db_month_perc_i = np.empty((no_rows, no_columns, 12))

    for month in range(1, 13):
        month_arr = np.empty((no_rows, no_columns, 0))
        for year in range(start.year, end.year + 1):
            days_of_month = calendar.monthrange(year, month)[1]
            lo_index = date_generated.index(datetime(year, month, 1))
            up_index = date_generated.index(datetime(year, month, days_of_month)) + 1
            month_arr = np.concatenate([month_arr, db['data'][:, :, lo_index:up_index]], -1)
        db_month_perc_i[:, :, month - 1] = np.percentile(month_arr, (100 - percentile), axis=2)
                  
    output_file = output_path + "threshold_monthly_" + variable + "_perc_" + str(percentile) + ".pickle"
    
    with open(output_file, 'wb') as handle:
        pickle.dump(db_month_perc_i, handle, protocol=pickle.HIGHEST_PROTOCOL)

def GetThresholdSeries(variable, db_file, percentile, window_length, polyorder, output_path):
    """
    CODE FOR GENERATING THRESHOLD SERIES FLATTENED AND SMOOTHED FOR LEAP AND REGULAR YEARS
    
    - src_filepath : "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/" (Absolute path)
    - reference_file : "0_P_CHIRPS.v2.0_mm-day-1_daily_2000.01.01_aligned.tif"
    - db : [row, column, month]
    - window_length : 45 (savgol_filter function)
    - polyorder: 3 (savgol_filter function)
    """
    
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    no_rows = db.shape[0]
    no_columns = db.shape[1]
    mask = np.isnan(db[:,:,0])
    
    flat_perc_i_regular_year = np.empty((no_rows, no_columns, 365))
    flat_perc_i_leap_year = np.empty((no_rows, no_columns, 366))
    
    smooth_perc_i_regular_year = np.empty((no_rows, no_columns, 365))
    smooth_perc_i_leap_year = np.empty((no_rows, no_columns, 366))
    
    start_regular_year = datetime.strptime("01-01-1979", "%d-%m-%Y")#reference regular year
    end_regular_year = datetime.strptime("31-12-1979", "%d-%m-%Y")
    date_generated_regular_year = [start_regular_year + timedelta(days=x) for x in range(0, (end_regular_year-start_regular_year).days + 1)]
    
    start_leap_year = datetime.strptime("01-01-1980", "%d-%m-%Y")#reference leap year
    end_leap_year = datetime.strptime("31-12-1980", "%d-%m-%Y")
    date_generated_leap_year = [start_leap_year + timedelta(days=x) for x in range(0, (end_leap_year-start_leap_year).days + 1)]
    
    i = 0
    j = 0
    for date in date_generated_regular_year:
        flat_perc_i_regular_year[:, :, i] = db[:, :, date.month - 1]
        i += 1
    for date in date_generated_leap_year:
        flat_perc_i_leap_year[:, :, j] = db[:, :, date.month - 1]
        j += 1
    
    offset_length = 3
    window_flat_perc_i_regular_year = np.empty((no_rows, no_columns, 365 * offset_length))
    for loop in range(offset_length):
        for day in range(365):
            window_flat_perc_i_regular_year[:, :, day + (365 * loop)] = flat_perc_i_regular_year[:, :, day]
    
    window_flat_perc_i_leap_year = np.empty((no_rows, no_columns, 366 * offset_length))
    for loop in range(offset_length):
        for day in range(366):
            window_flat_perc_i_leap_year[:, :, day + (366 * loop)] = flat_perc_i_leap_year[:, :, day]
            
    window_smooth_perc_i_regular_year = np.empty((no_rows, no_columns, 365 * offset_length))
    window_smooth_perc_i_leap_year = np.empty((no_rows, no_columns, 366 * offset_length))
        
    window_flat_perc_i_regular_year[mask] = 0
    window_flat_perc_i_leap_year[mask] = 0
    
    window_smooth_perc_i_regular_year = savgol_filter(window_flat_perc_i_regular_year, window_length, polyorder, axis=-1) # window size 51, polynomial order 3
    window_smooth_perc_i_leap_year = savgol_filter(window_flat_perc_i_leap_year, window_length, polyorder, axis=-1) # window size 51, polynomial order 3
        
    window_smooth_perc_i_regular_year[mask] = np.nan
    window_smooth_perc_i_leap_year[mask] = np.nan
    
    smooth_perc_i_regular_year[:, :, :] = window_smooth_perc_i_regular_year[:, :, 365:365*2] # window size 51, polynomial order 3
    smooth_perc_i_leap_year[:, :, :] = window_smooth_perc_i_leap_year[:, :, 366:366*2] # window size 51, polynomial order 3
        
    output_files = [output_path + "flattened_threshold_monthly_perc_" + str(percentile) + "_regular_year.pickle",
                    output_path + "flattened_threshold_monthly_perc_" + str(percentile) + "_leap_year.pickle",
                    output_path + "smoothed_threshold_monthly_perc_" + str(percentile) + "_regular_year.pickle",
                    output_path + "smoothed_threshold_monthly_perc_" + str(percentile) + "_leap_year.pickle"]
    
    export_dbs = [flat_perc_i_regular_year, 
                  flat_perc_i_leap_year, 
                  smooth_perc_i_regular_year, 
                  smooth_perc_i_leap_year]

    for db_ex, output_file in zip(export_dbs, output_files):
        with open(output_file, 'wb') as handle:
            pickle.dump(db_ex, handle, protocol=pickle.HIGHEST_PROTOCOL)

def BinaryDroughtPercentile(variable, percentile, db_file, smoothed_threshold, output_path):
    """
    CODE FOR CALCULATING BINARY REPRESENTATION OF DROUGHT ACCORDING TO THE GIVEN PERCENTILE OF THE CODE ABOVE. EXPORTED TO A DATABASE
    
    - start_date : "01-01-2000"
    - end_date : "31-12-2011"
    - src_filepath : "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/" (Absolute path)
    - reference_file : "0_P_CHIRPS.v2.0_mm-day-1_daily_2000.01.01_aligned.tif"
    - db : [row, column, year, month, day]
    - smoothed_threshold : [smooth_perc_i_leap_year, smooth_perc_i_regular_year]
    """
    
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    with open(smoothed_threshold[0], 'rb') as handle:
        smooth_perc_i_leap_year = pickle.load(handle)
    
    with open(smoothed_threshold[1], 'rb') as handle:
        smooth_perc_i_regular_year = pickle.load(handle)
    
    start = db['start']
    end = db['end']
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]  
   
    mask = np.isnan(db['data'][:,:,0])

    drought_binary_db = {}
    c = 0
    i = 0
    for date in date_generated:
        if calendar.isleap(date.year):
            drought_binary_db[date] = (np.invert((db['data'][:, :, c] - smooth_perc_i_leap_year[:, :, i]) >= 0)).astype(np.float64)
            drought_binary_db[date][mask] = np.nan
            c += 1
        else:
            drought_binary_db[date] = (np.invert((db['data'][:, :, c] - smooth_perc_i_regular_year[:, :, i]) >= 0)).astype(np.float64)
            drought_binary_db[date][mask] = np.nan
            c += 1
        if date.year == (date + timedelta(days=1)).year:
            i += 1
        else:
            i = 0
    
    output_file = output_path + "drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
    
    with open(output_file, 'wb') as handle:
        pickle.dump(drought_binary_db, handle, protocol=pickle.HIGHEST_PROTOCOL)     

def SDI(db, interval):
    """
    - db : [row, columns, year, month] or [row, column, flattened series]
    - interval : 1, 3, 6
    """
    
    # assert len(db['data'].shape) >= 3, 'Dimension of DataBase has to be greater than 3. [row, column, year, month] or [row, column, flattened series]'
    assert type(interval) == int, 'Interval value has to be integer. This is for calculating e.g. SDI1, SDI3, SDI6...'
        
    no_rows = db['data'].shape[0]
    no_columns = db['data'].shape[1]
    no_data = db['data'].shape[2]
    
    sdi = np.full((no_rows, no_columns, no_data), np.nan)
    variable_accum = np.full((no_rows, no_columns, no_data), np.nan)
    ln_array = np.full((no_rows, no_columns, no_data), np.nan)
    h_gamma = np.full((no_rows, no_columns, no_data), np.nan)
    
    for i in range(interval, no_data + 1):
        variable_accum[:, :, i - 1] = np.nansum(db['data'][:, :, i - interval : i], axis = 2)
    
    np.seterr(divide = 'ignore')
    np.seterr(invalid = 'ignore')
    ln_array = np.where(variable_accum!=np.float64(0), np.log(variable_accum), 0)
    
    m_zeros = np.count_nonzero(variable_accum==np.float64(0), axis=2).astype(np.float64)
    n = variable_accum.shape[2] - interval + 1
    q = m_zeros/float(n)
    miu = np.nansum(variable_accum, axis=2) / n
    A = np.log(miu) - np.nansum(ln_array, axis=2) / n
    alpha = (1 / (4 * A)) * (1 + (1 + (4 * A) / 3) ** 0.5)
    beta = miu / alpha
    
    for i in range(interval, no_data + 1):
        h_gamma[:, :, i - 1] = (1 - q) * gamma.cdf(variable_accum[:, :, i - 1], a=alpha, scale=beta) + q
        sdi[:, :, i - 1] = norm.ppf(h_gamma[:, :, i - 1])
    
    return sdi

def DroughtEvents(db, threshold=-1):
    """
    - db : [row, columns, flattened series]
    - threshold : -1
    """
    
    assert len(db.shape) == 3, 'Dimension of DataBase has to be 3. [row, column, flattened series].'
    assert type(threshold) == int and threshold < 0, 'Threshold value has to be integer and less than zero.'
    np.seterr(invalid = 'ignore')

    no_rows = db.shape[0]
    no_columns = db.shape[1]
    no_data = db.shape[2]
        
    mask = np.isnan(db[:, :, -1])

    stats = np.array(np.full((no_rows, no_columns), np.nan), dtype=object)
    state = np.full((no_rows, no_columns, no_data), np.nan)
    magnitude = np.full((no_rows, no_columns, no_data), np.nan)
    duration = np.full((no_rows, no_columns, no_data), np.nan)
    
    np.seterr(invalid = 'ignore')
    state = np.array(np.where(db<=threshold, 1, 0), dtype=float)
    state[mask] = np.nan
    
    sdi_events = abs(state * db)
    
    for row in range(no_rows):
        for column in range(no_columns):
            value_array = np.array(sdi_events[row, column, :])
            value_array[np.isinf(value_array)] = 0
            value_array[np.isneginf(value_array)] = 0
            if np.isnan(value_array).all() == True:
                continue
            
            event_array = np.array(state[row, column, :])
            
            group_values = []
            group_events = []
            sum_group_events = 0
            sum_group_values = 0
            
            for i in range(len(value_array)):
                value = value_array[i]
                event = event_array[i]
        
                if value != 0 and np.isnan(value) == False:
                    try:
                        if value_array[i + 1] == 0:
                            sum_group_values += value
                            sum_group_events += event
                            group_values.append(sum_group_values)
                            group_events.append(sum_group_events)
                            sum_group_events = 0
                            sum_group_values = 0
                        else:
                            sum_group_values += value
                            sum_group_events += event
                            group_values.append(0)
                            group_events.append(0)
                    except:
                        pass
                else:
                    group_values.append(value)
                    group_events.append(event)
            
            group_values = np.array(group_values)
            group_events = np.array(group_events)
            
            group_values_array = np.array([i for i in group_values if (np.isnan(i)==False and i!=np.float64(0))])
            group_events_array = np.array([i for i in group_events if (np.isnan(i)==False and i!=np.float64(0))])
            
            magnitude[row, column, :len(group_values_array)] = group_values_array
            duration[row, column, :len(group_events_array)] = group_events_array
                        
            if len(group_events_array) == 0 or np.isnan(group_events_array).all():
                stats_dict = {}
                stats_dict = {'No_events' : 0,
                              'Magnitude_mean' : 0,
                              'Magnitude_standard_deviation' : 0, 
                              'Magnitude_max' : 0,
                              'Magnitude_min' : 0,
                              'Duration_mean' : 0,
                              'Duration_standard_deviation' : 0,
                              'Duration_max' : 0,
                              'Duration_min' : 0}
            
            if len(group_events_array) == 1:
                stats_dict = {}
                stats_dict = {'No_events' : 1,
                              'Magnitude_mean' : group_values_array[0],
                              'Magnitude_standard_deviation' : 0, 
                              'Magnitude_max' : group_values_array[0],
                              'Magnitude_min' : group_values_array[0],
                              'Duration_mean' : 1,
                              'Duration_standard_deviation' : 0,
                              'Duration_max' : 1,
                              'Duration_min' : 1}
            
            if len(group_events_array) > 1:
                stats_dict = {}
                stats_dict = {'No_events' : len(group_events_array),
                              'Magnitude_mean' : np.mean(group_values_array),
                              'Magnitude_standard_deviation' : np.std(group_values_array, ddof=1), 
                              'Magnitude_max' : np.max(group_values_array),
                              'Magnitude_min' : np.min(group_values_array),
                              'Duration_mean' : np.mean(group_events_array),
                              'Duration_standard_deviation' : np.std(group_events_array, ddof=1),
                              'Duration_max' : np.max(group_events_array),
                              'Duration_min' : np.min(group_events_array)}
                
            stats[row, column] = stats_dict
            
    return stats, state, magnitude, duration

def MultipleSDICalculation(sdi_names, dbs_path, intervals, output_path):
    """
    - dbs : {'SPI' : {'DB' : db_prec},
             'SRI' : {'DB' : db_runoff},
             'SSI' : {'DB' : db_soilmoisture}}
    - intervals : [1, 3, 6]
    """
    
    dbs = {}
    
    for sdi, sdi_path in zip(sdi_names, dbs_path):
        with open(sdi_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[sdi] = db
        db = None
    
    period = [dbs[sdi_names[0]]['start'], dbs[sdi_names[0]]['end']]
    
    for key in dbs.keys():
        sdi_db = {}
        sdi_db['start'] = period[0]
        sdi_db['end'] = period[1]
        sdi_db[key] = {}
        for i in intervals:
            interval_key = key + str(i)
            
            if key == 'SEDI':
                sdi_db[key][interval_key] = {interval_key : SDI(dbs[key], i)}
                sdi_db[key][interval_key][interval_key] *= -1
            else:
                sdi_db[key][interval_key] = {interval_key : SDI(dbs[key], i)}
                        
            stats, state, magnitude, duration = DroughtEvents(sdi_db[key][interval_key][interval_key])
            
            stats_key = interval_key + '_Stats'
            state_key = interval_key + '_State' 
            magnitude_key = interval_key + '_Magnitude'
            duration_key = interval_key + '_Duration'
            
            sdi_db[key][interval_key][stats_key] = stats
            sdi_db[key][interval_key][state_key] = state
            sdi_db[key][interval_key][magnitude_key] = magnitude
            sdi_db[key][interval_key][duration_key] = duration

        output_file = output_path + key + ".pickle"

        with open(output_file, 'wb') as handle:
            pickle.dump(sdi_db, handle, protocol=pickle.HIGHEST_PROTOCOL)   
        
        del sdi_db, stats, state, magnitude, duration
    
    dbs = None

def NCDACleaning(variable, percentile, db_file, output_path, min_size=20, connectivity=1):
    
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    start = min(db.keys())
    end = max(db.keys())
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]  
    
    drought_binary_db = {}
    
    for  date in date_generated:
        mask_nan = np.isnan(db[date])
        db[date][mask_nan] = 0
        db[date] = db[date].astype(np.int)
        drought_binary_db[date] = remove_small_objects(db[date].astype(bool), min_size, connectivity)
        drought_binary_db[date] = ~drought_binary_db[date]
        drought_binary_db[date] = remove_small_objects(drought_binary_db[date], min_size, connectivity)
        drought_binary_db[date] = ~drought_binary_db[date]
        drought_binary_db[date] = drought_binary_db[date].astype(np.float64)
        drought_binary_db[date][mask_nan] = np.nan
    
    output_file = output_path + "drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
    
    with open(output_file, 'wb') as handle:
        pickle.dump(drought_binary_db, handle, protocol=pickle.HIGHEST_PROTOCOL)   

def ExportRastersFromDB(variable, percentile, db_file, reference_raster, output_path, pixel_type=1):
      
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    start = min(db.keys())
    end = max(db.keys())
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    
    for date in date_generated:
        fulldate = str(date.strftime("%Y_%m_%d"))
        dst_file = output_path + "/" + variable + "_binary_drought_perc_" + str(percentile) + "_" + fulldate + ".tif"
        db[date][arr == noval] = noval
        # db[date][arr == noval] = np.nan
        RasterLike(raster, db[date], dst_file, pixel_type=pixel_type)
        
def ExportSDIStatsRasters(sdi, i, db_file, reference_raster, output_path):
    
    with open(db_file, 'rb') as handle:
        sdi_db = pickle.load(handle)
        
    raster = gdal.Open(reference_raster)
        
    interval_key = sdi + str(i)
    stats_key = interval_key + '_Stats'
    no_rows = sdi_db[sdi][interval_key][interval_key].shape[0]
    no_columns = sdi_db[sdi][interval_key][interval_key].shape[1]
    stat_i = np.full((no_rows, no_columns), np.nan)

    stats = ['No_events',
             'Magnitude_mean',
             'Magnitude_standard_deviation', 
             'Magnitude_max',
             'Magnitude_min',
             'Duration_mean',
             'Duration_standard_deviation',
             'Duration_max',
             'Duration_min']
    
    for stat in stats:
        for row in range(no_rows):
            for column in range(no_columns):
                if pd.isnull(np.array(sdi_db[sdi][interval_key][stats_key][row, column], dtype=object)):
                    continue
                stat_i[row, column] = sdi_db[sdi][interval_key][stats_key][row, column][stat]
    
        dst_file = output_path + "/" + interval_key + "_" + stat + ".tif"
        RasterLike(raster, stat_i, dst_file)
            
def MultipleExportSDIStatsRasters(sdi_names, intervals, db_files, reference_raster, output_paths):
    
    for db, sdi, output in zip(db_files, sdi_names, output_paths):
        for i in intervals:
            ExportSDIStatsRasters(sdi, i, db, reference_raster, output)
        

def DroughtMultipleElevations(variable, percentile, dem_path, db_path, dict_elev, output_path):
    
    with open(db_path, 'rb') as handle:
        db = pickle.load(handle)
    
    start = min(db.keys())
    end = max(db.keys())
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

    dem = gdal.Open(dem_path)
    arr_dem = dem.GetRasterBand(1).ReadAsArray()
    dem = None
    
    drought_soil_db = {}
    drought_soil_db['elevations'] = dict_elev
    drought_soil_db['data'] = {}
    
    for date in date_generated:
        drought_soil_db['data'][date] = {}
        for soil_type, soil_range in dict_elev.items():
            mask = ((soil_range[0] <= arr_dem) & (arr_dem < soil_range[1])).astype(int)
            drought_soil_db['mask_' + soil_type] = mask
            drought_soil_db['data'][date][soil_type] = db[date] * mask
    
    output_file = output_path + "drought_binary_thermal_floors_" + variable + "_perc_" + str(percentile) + ".pickle"
    
    with open(output_file, 'wb') as handle:
        pickle.dump(drought_soil_db, handle, protocol=pickle.HIGHEST_PROTOCOL)   

    
def DroughtMultipleAreas(variable, percentile, areas_path, db_path, area_column_name, codes_file, output_path):
    
    with open(db_path, 'rb') as handle:
        db = pickle.load(handle)
    
    start = min(db.keys())
    end = max(db.keys())
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    dict_codes = pd.read_excel(codes_file).set_index(area_column_name).T.to_dict('records')[0]
    
    drought_soil_db = {}
    drought_soil_db['areas'] = dict_codes
    drought_soil_db['data'] = {}

    areas = gdal.Open(areas_path)
    arr_areas = areas.GetRasterBand(1).ReadAsArray()
    areas = None

    for date in date_generated:
        drought_soil_db['data'][date] = {}
        for area, code in dict_codes.items():
            mask = (arr_areas == code).astype(int)
            if (mask == 0).all():
                continue
            drought_soil_db['mask_' + area] = mask
            drought_soil_db['data'][date][area] = db[date] * mask
    
    output_file = output_path + "drought_binary_areas_" + variable + "_perc_" + str(percentile) + ".pickle"
    
    with open(output_file, 'wb') as handle:
        pickle.dump(drought_soil_db, handle, protocol=pickle.HIGHEST_PROTOCOL)   
    
    
def ExportRastersSDI(sdi, intervals, db_file, reference_raster, grl_output_path):
    
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    start = db['start']
    end = db['end']
    
    date_generated = pd.to_datetime(pd.date_range(str(start.strftime("%Y-%m-%d")),str(end.strftime("%Y-%m-%d")), freq='MS'))
    date_generated = [date_generated[i].date() for i in range(len(date_generated))]
    
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    
    for interval in intervals:
        output_path = grl_output_path + "/" + sdi + "/" + sdi + str(interval) + "/values"
        for date, c in zip(date_generated, range(len(date_generated))):
            fulldate = str(date.strftime("%Y_%m_%d"))
            dst_file = output_path + "/" + sdi + str(interval) + "_value_" + fulldate + ".tif"
            db[sdi][sdi + str(interval)][sdi + str(interval)][:,:,c][arr == noval] = noval
            RasterLike(raster, db[sdi][sdi + str(interval)][sdi + str(interval)][:,:,c], dst_file)


def SDIClasses(sdi_names, dbs_path, intervals, output_path):
    
    """
    - dbs : {'SPI' : {'DB' : db_prec},
             'SRI' : {'DB' : db_runoff},
             'SSI' : {'DB' : db_soilmoisture}}
    - intervals : [1, 3, 6]
    """
    
    dbs = {}
    
    for sdi, sdi_path in zip(sdi_names, dbs_path):
        with open(sdi_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[sdi] = db
        db = None
    
    period = [dbs[sdi_names[0]]['start'], dbs[sdi_names[0]]['end']]
    
    for key in dbs.keys():
        sdi_db = {}
        sdi_db['start'] = period[0]
        sdi_db['end'] = period[1]
        sdi_db[key] = {}
        classes_dict = {}
        classes_dict['start'] = period[0]
        classes_dict['end'] = period[1]
        classes_dict[key] = {}
        for i in intervals:
            interval_key = key + str(i)
            
            if key == 'SEDI':
                sdi_db[key][interval_key] = {interval_key : SDI(dbs[key], i)}
                sdi_db[key][interval_key][interval_key] *= -1
            else:
                sdi_db[key][interval_key] = {interval_key : SDI(dbs[key], i)}
            
            no_rows = sdi_db[key][interval_key][interval_key].shape[0]
            no_cols = sdi_db[key][interval_key][interval_key].shape[1]
            no_data = sdi_db[key][interval_key][interval_key].shape[2]
            
            classes_db = np.empty((no_rows, no_cols, no_data))
            
            classes_db[sdi_db[key][interval_key][interval_key] <= -2] = 0
            classes_db[(sdi_db[key][interval_key][interval_key] > -2)* (sdi_db[key][interval_key][interval_key] <= -1.5)] = 1
            classes_db[(sdi_db[key][interval_key][interval_key] > -1.5)* (sdi_db[key][interval_key][interval_key] <= -1)] = 2
            classes_db[(sdi_db[key][interval_key][interval_key] > -1)* (sdi_db[key][interval_key][interval_key] <= 1)] = 3
            classes_db[(sdi_db[key][interval_key][interval_key] > 1)* (sdi_db[key][interval_key][interval_key] <= 1.5)] = 4
            classes_db[(sdi_db[key][interval_key][interval_key] > 1.5)* (sdi_db[key][interval_key][interval_key] <= 2)] = 5
            classes_db[sdi_db[key][interval_key][interval_key] > 2] = 6
            
            classes_db[np.isnan(sdi_db[key][interval_key][interval_key])] = np.nan
            
            classes_dict[key][interval_key] = classes_db

        output_file = output_path + key + "_classes.pickle"

        with open(output_file, 'wb') as handle:
            pickle.dump(classes_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)   
        
        del classes_dict
    
    dbs = None
    

def ExportRastersSDIClasses(sdi, intervals, db_file, reference_raster, grl_output_path):
    
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    start = db['start']
    end = db['end']
    
    date_generated = pd.to_datetime(pd.date_range(str(start.strftime("%Y-%m-%d")),str(end.strftime("%Y-%m-%d")), freq='MS'))
    date_generated = [date_generated[i].date() for i in range(len(date_generated))]
    
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()

    for interval in intervals:
        output_path = grl_output_path + "/" + sdi + "/" + sdi + str(interval) + "/classes"
        for date, c in zip(date_generated, range(len(date_generated))):
            fulldate = str(date.strftime("%Y_%m_%d"))
            dst_file = output_path + "/" + sdi + str(interval) + "_classes_" + fulldate + ".tif"
            db[sdi][sdi + str(interval)][:,:,c][arr == noval] = noval
            RasterLike(raster, db[sdi][sdi + str(interval)][:,:,c], dst_file)
            

def ExportBinaryRastersSDI(sdi, intervals, db_file, reference_raster, grl_output_path):
    
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    start = db['start']
    end = db['end']
    
    date_generated = pd.to_datetime(pd.date_range(str(start.strftime("%Y-%m-%d")),str(end.strftime("%Y-%m-%d")), freq='MS'))
    date_generated = [date_generated[i].date() for i in range(len(date_generated))]
    
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    
    for interval in intervals:
        output_path = grl_output_path + "/" + sdi + "/" + sdi + str(interval) + "/binary"
        for date, c in zip(date_generated, range(len(date_generated))):
            fulldate = str(date.strftime("%Y_%m_%d"))
            dst_file = output_path + "/" + sdi + str(interval) + "_binary_drought_" + fulldate + ".tif"
            db[sdi][sdi + str(interval)][sdi + str(interval) + "_State"][:,:,c][arr == noval] = noval
            RasterLike(raster, db[sdi][sdi + str(interval)][sdi + str(interval) + "_State"][:,:,c], dst_file)
         
def CDAAnalysis(variable, percentile, db_file, output_path):
    
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    start = min(db.keys())
    end = max(db.keys())
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]  
    
    drought_clusters_db = {}
    
    for date in date_generated:
        raster_arr = np.array(db[date], dtype=np.uint8)
        num_labels, labels_im = cv2.connectedComponents(raster_arr)
        drought_clusters_db[date] = {}
        drought_clusters_db[date]['Number_of_clusters'] = num_labels
        drought_clusters_db[date]['data'] = labels_im
        
    output_file = output_path + "drought_clusters_" + variable + "_perc_" + str(percentile) + ".pickle"
    
    with open(output_file, 'wb') as handle:
        pickle.dump(drought_clusters_db, handle, protocol=pickle.HIGHEST_PROTOCOL)     

def ExportRastersFromCDADB(variable, percentile, db_file, reference_raster, output_path, pixel_type=1):
      
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    start = min(db.keys())
    end = max(db.keys())
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    
    for date in date_generated:
        fulldate = str(date.strftime("%Y_%m_%d"))
        dst_file = output_path + "/" + variable + "_clusters_drought_perc_" + str(percentile) + "_" + fulldate + ".tif"
        db[date]['data'][arr == noval] = noval
        RasterLike(raster, db[date]['data'], dst_file, pixel_type=pixel_type)

    
    
    
