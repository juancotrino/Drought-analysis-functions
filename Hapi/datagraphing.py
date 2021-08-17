# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:18:52 2020

@author: juanmanuel
"""

import pickle
import random
import numpy as np
import pandas as pd
import scipy.stats as scistat
import hydroeval as he
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import gdal
from datetime import datetime, timedelta
import calendar
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as colors
from matplotlib import cm
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1 import make_axes_locatable

import Hapi.giscatchment as GC


def ThresholdAnalysisGraphing(variable_name, variable_unit, percentile, db_path, 
                              threshold_series, year, row, column, dst_path=None, dpi=600):
    """
    CODE FOR GRAPHING THRESHOLD DROUGHT ANALYSIS IN A GIVEN CELL AND GIVEN YEAR
    
    - variable_name : "Runoff"
    - variable_unit : "mm/s"
    - start_date : "01-01-2000"
    - end_date : "31-12-2011"
    - db_path : "/Users/juanmanuel/Desktop/RUNOFF_DBs/runoff_db.npy"
    - threshold_series : [path + "flattened_threshold_monthly_p85_leap_year.npy",
                          path + "smoothed_threshold_monthly_p85_leap_year.npy",
                          path + "flattened_threshold_monthly_p85_regular_year.npy",
                          path + "smoothed_threshold_monthly_p85_regular_year.npy"]
    - year : 2011
    - row : 80
    - column : 50
    - dst_path : "/Users/juanmanuel/Desktop/RUNOFF_DBs/"
    """
    
    print_var = variable_name.title().replace("_", " ")
    
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    with open(db_path, 'rb') as handle:
        db = pickle.load(handle)
        
    with open(threshold_series[0], 'rb') as handle:
        y_perc_i_leap_year = pickle.load(handle)

    with open(threshold_series[1], 'rb') as handle:
        smooth_perc_i_leap_year = pickle.load(handle)

    with open(threshold_series[2], 'rb') as handle:
        y_perc_i_regular_year = pickle.load(handle)

    with open(threshold_series[3], 'rb') as handle:
        smooth_perc_i_regular_year = pickle.load(handle)
            
    y_data = np.array([])
    start_index = (start - db['start']).days
    end_index = start_index + len(date_generated)

    for i in range(start_index, end_index):
        y_data = np.append(y_data, db['data'][row, column, i])
        
    plt.figure(figsize=(17,4))

    if calendar.isleap(year):
        x = date_generated
        plt.plot(x, y_data, '-C0', label=print_var)
        plt.plot(x, y_perc_i_leap_year[row, column, :], '--C3', label=str(percentile)+' Percentile')
        plt.plot(x, smooth_perc_i_leap_year[row, column, :], 'C2', label='Threshold')
        title = "Behaviour of " + print_var + " in cell r" + str(row) + "c" + str(column) + " in " + str(year) + " (leap) (percentile " + str(percentile) + ")"
    else:
        x = date_generated
        plt.plot(x, y_data, '-C0', label=print_var)
        plt.plot(x, y_perc_i_regular_year[row, column, :], '--C3', label=str(percentile)+' Percentile')
        plt.plot(x, smooth_perc_i_regular_year[row, column, :], 'C2', label='Threshold')
        title = "Behaviour of " + print_var + " in cell r" + str(row) + "c" + str(column) + " in " + str(year) +  " (percentile " + str(percentile) + ")"
    
    locator = mdates.MonthLocator()
    fmt = mdates.DateFormatter('%b')
    
    X = plt.gca().xaxis
    X.set_major_locator(locator)
    X.set_major_formatter(fmt)
    
    plt.legend()
    xlabel = "Months"
    ylabel = print_var + " [" + variable_unit + "]"
    plt.title(title, pad=30, fontsize=20)
    plt.xlabel(xlabel, fontdict=None, labelpad=None)
    plt.ylabel(ylabel, fontdict=None, labelpad=None)
    
    if dst_path != None:
        plt.savefig(dst_path + "Graph_analysis_Threshold_perc_" + str(percentile) + "_" + variable_name + "_" + str(year) + "_r" + str(row) + "_c" + str(column) + ".pdf", dpi=dpi, bbox_inches='tight')
    
    plt.show
    
def SDIAnalysisGraphing(sdi_names, sdi_interval_analysis, dbs_path, row, column, 
                        sdi_threshold = -1, dst_path=None, dpi=600):
    
    dbs = {}
        
    for sdi, sdi_path in zip(sdi_names, dbs_path):
        with open(sdi_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[sdi] = db
        db = None
    
    start = dbs[sdi_names[0]]['start']
    end = dbs[sdi_names[0]]['end']
    
    date_generated = pd.date_range(start, end, freq='1M')-pd.offsets.MonthBegin(1)
    plt.figure(figsize=(17,4))
    
    edge_value = []
    sdi_print = []
    for sdi_name in sdi_names:
        for interval in sdi_interval_analysis:
            y_data = dbs[sdi_name][sdi_name][sdi_name + str(interval)][sdi_name + str(interval)][row, column, :]
            x = date_generated
            sdi_print.append(sdi_name + str(interval))
            plt.plot(x, y_data, label=sdi_name + str(interval))
            edge_value.append(np.max(([np.nanmax(y_data), abs(np.nanmin(y_data))])))
    
    x_threshold = [start, end]
    y_threshold = [sdi_threshold, sdi_threshold]
    plt.plot(x_threshold, y_threshold, linewidth=0.5, color='C3')
    
    plt.axhline(0, color='k', linewidth=0.5)
    
    edge_value = np.max(edge_value)
    plot_y_edge = edge_value * 1.20
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,-plot_y_edge,plot_y_edge))
    
    locator = mdates.YearLocator()
    fmt = mdates.DateFormatter('%Y')
    
    X = plt.gca().xaxis
    X.set_major_locator(locator)
    X.set_major_formatter(fmt)
        
    plt.legend()
    xlabel = "Year"
    
    if len(sdi_names) == 1:
        title = "Behaviour of " + sdi_names[0] + " in cell r" + str(row) + "c" + str(column)
        ylabel = sdi_names[0]
    else:
        title = "Behaviour of " + ', '.join(sdi_print) + " in cell r" + str(row) + "c" + str(column)
        ylabel = ', '.join(sdi_print)
    
    plt.title(title, pad=30, fontsize=20)
    plt.xlabel(xlabel, fontdict=None, labelpad=None)
    plt.ylabel(ylabel, fontdict=None, labelpad=None)

    if dst_path != None:
        plt.savefig(dst_path + "Graph_analysis_" + str(sdi_names) + str(sdi_interval_analysis) + "_r" + str(row) + "_c" + str(column) + ".pdf", dpi=dpi, bbox_inches='tight')
    
    plt.show

def ModelResultsGraphing(variable, variable_unit, db_observed, obs_sheet, coor_sheet, db_simulated, 
                         row, column, ref_raster, start_date=None, end_date=None, valid_start_date=None,
                         dst_path=None, dpi=600):
    
    with open(db_simulated, 'rb') as handle:
        db = pickle.load(handle)
    
    if start_date == None and end_date == None:
        start = db['start']
        end = db['end']
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
    
    start_index = (start - db['start']).days
    end_index = (end - db['start']).days + 1
        
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    raster = gdal.Open(ref_raster)
    
    obs_data = pd.read_excel(db_observed, sheet_name=obs_sheet, convert_float=True, index_col=0)
    obs_data.index = pd.to_datetime(obs_data.index)
    obs_data.columns = obs_data.columns.map(str)
    obs_data = obs_data.loc[start:end]
    
    stations = pd.read_excel(db_observed, sheet_name=coor_sheet, convert_float=True)
    coordinates = stations[['id','x','y','weight']][:]
    coordinates.loc[:, ["cell_row", "cell_col"]] = GC.NearestCell(raster, coordinates)
    coordinates = coordinates.set_index('id')
    coordinates.index = coordinates.index.map(str)
    
    plt.figure(figsize=(17,4))
    
    x = date_generated
    if valid_start_date == None:
        y_data = db['data'][row, column, start_index:end_index]
        plt.plot(x, y_data, label='Simulated', color='C3')
    else:
        valid = datetime.strptime(valid_start_date, "%d-%m-%Y")
        valid_start_index = (valid - db['start']).days + 1
        y_calib_data = db['data'][row, column, start_index:valid_start_index]
        y_valid_data = db['data'][row, column, valid_start_index:end_index]
        x_calib = [start + timedelta(days=x) for x in range(0, (valid-start).days + 1)]
        x_valid = [valid + timedelta(days=x) for x in range(0, (end-valid).days)]
        plt.plot(x_calib, y_calib_data, label='Simulated (Calibration)', color='C3')
        plt.plot(x_valid, y_valid_data, label='Simulated (Validation)', color='C2')
    
    calib_point = [row, column]
    
    if (coordinates[['cell_row','cell_col']].values == calib_point).all(axis=1).any() and variable == 'runoff':
        station = coordinates[(coordinates[['cell_row','cell_col']].values == calib_point).all(axis=1)].index[0]
        y_data_obs = obs_data[[station]]
        plt.plot(x, y_data_obs, label='Observed', color='C0')
        
        df = pd.DataFrame()
        df['obs'] = list(y_data_obs.to_numpy().ravel())
        df['sim'] = [*y_calib_data, *y_valid_data]
        df = df.dropna()
        
        rmse = mean_squared_error(df['obs'], df['sim'], squared=False)
        nse = he.evaluator(he.nse, df['sim'], df['obs'])
        mae = mean_absolute_error(df['obs'], df['sim'])
        r = np.corrcoef(df['obs'], df['sim'])[0, 1]
        print("RMSE r" + str(row) + "_c" + str(column) + ": " + str(rmse))
        print("NSE r" + str(row) + "_c" + str(column) + ": " + str(nse))
        print("MAE r" + str(row) + "_c" + str(column) + ": " + str(mae))
        print("Cor r" + str(row) + "_c" + str(column) + ": " + str(r))

       
    locator = mdates.YearLocator()
    fmt = mdates.DateFormatter('%Y')

    X = plt.gca().xaxis
    X.set_major_locator(locator)
    X.set_major_formatter(fmt)
    
    print_variable = variable.capitalize().replace("_"," ")
    
    plt.legend()
    title = print_variable + " results in cell r" + str(row) + "c" + str(column)
    xlabel = "Year"
    ylabel = print_variable + " [" + variable_unit + "]"
    
    plt.title(title, pad=30, fontsize=20)
    plt.xlabel(xlabel, fontdict=None, labelpad=None)
    plt.ylabel(ylabel, fontdict=None, labelpad=None)

    if dst_path != None:
        plt.savefig(dst_path + "Graph_analysis_Model_results_" + variable + "_r" + str(row) + "_c" + str(column) + ".pdf", dpi=dpi, bbox_inches='tight')
    
    plt.show
    
def MonthlyDataGraphing(variable, dbs_path, row, column, value=0, dst_path=None, dpi=600):
    
    with open(dbs_path, 'rb') as handle:
        db = pickle.load(handle)
                
    months = [i for i in range(12)]
    
    plt.figure(figsize=(10,5))    
        
    monthly_value = []
    
    for month in months:
        monthly_arr = []
        months_num_arr = [i for i in range(month, db['data'].shape[2], 12)]
        for m in months_num_arr:
            monthly_arr.append(db['data'][row, column, m])
        if value == 0:
            monthly_value.append(np.mean(monthly_arr))
        if value == 1:
            monthly_value.append(np.min(monthly_arr))
        if value == 2:
            monthly_value.append(np.max(monthly_arr))

    month_text = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    
    plt.bar(months, monthly_value)
    plt.xticks(np.arange(12), month_text)
    
    print_variable = variable.title().replace("_"," ")
    plt.ylabel(print_variable + ' [m3/s]', fontdict=None, labelpad=None)
    plt.xlabel('Month', fontdict=None, labelpad=None)
    if value == 0:
        plt.title('Average monthly ' + print_variable + " in cell r" + str(row) + "c" + str(column), pad=30, fontsize=20)
    if value == 1:
        plt.title('Monthly minimum ' + print_variable + " in cell r" + str(row) + "c" + str(column), pad=30, fontsize=20)
    if value == 2:
        plt.title('Monthly maximum ' + print_variable + " in cell r" + str(row) + "c" + str(column), pad=30, fontsize=20)
    
    if dst_path != None:
        if value == 0:
            plt.savefig(dst_path + "Graph_analysis_Average_monthly_" + variable + "_r" + str(row) + "c" + str(column) + ".pdf", dpi=dpi, bbox_inches='tight')
        if value == 1:
            plt.savefig(dst_path + "Graph_analysis_Monthly_minimum_" + variable + "_r" + str(row) + "c" + str(column) + ".pdf", dpi=dpi, bbox_inches='tight')
        if value == 2:
            plt.savefig(dst_path + "Graph_analysis_Monthly_maximum_" + variable + "_r" + str(row) + "c" + str(column) + ".pdf", dpi=dpi, bbox_inches='tight')

    plt.show()


def PDAGraphing(variable, percentiles, dbs_path, analysis_names, start_date=None, end_date=None, 
                separated=0, dst_path=None, dpi=600):
    
    dbs = {}
    
    for db_path, percentile in zip(dbs_path, percentiles):
        with open(db_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[percentile] = db
        db = None
    
    if start_date == None and end_date == None:
        start = min(dbs[percentiles[0]].keys())
        end = max(dbs[percentiles[0]].keys())
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
            
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    no_cells = np.count_nonzero(~np.isnan(dbs[percentiles[0]][start]))
    
    if separated == 0:
        plt.figure(figsize=(17,4))
        for analysis in analysis_names:
            for percentile in percentiles:
                pda_arr = []
                db = dbs[percentile]
                for date in date_generated:
                    arr = db[date]
                    zeros = np.count_nonzero(arr==0)
                    pda_i = ((no_cells - zeros) / no_cells) * 100
                    pda_arr.append(pda_i)
                
                plt.plot(date_generated, pda_arr, label='PDA - ' + analysis + ' - Percentile ' + str(percentile))
                
        locator = mdates.YearLocator()
        fmt = mdates.DateFormatter('%Y')
    
        X = plt.gca().xaxis
        X.set_major_locator(locator)
        X.set_major_formatter(fmt)
        
        plt.ylim(-5, 105)
        
        print_variable = variable.title().replace("_"," ")
        
        plt.legend()
        if len(analysis_names) > 1:
            title = "Percentage Drought Area (" + print_variable + ")"
        else:
            title = "Percentage Drought Area (" + print_variable + " - " + analysis + ")"
       
        xlabel = "Year"
        ylabel = "PDA [%]"
        
        plt.title(title, pad=30, fontsize=20)
        plt.xlabel(xlabel, fontdict=None, labelpad=None)
        plt.ylabel(ylabel, fontdict=None, labelpad=None)
    
        if dst_path != None:
            plt.savefig(dst_path + "Graph_analysis_PDA_percentiles_" + variable + ".pdf", dpi=dpi, bbox_inches='tight')
        
        plt.show
    
    if separated == 1:
        for analysis in analysis_names:
            for percentile in percentiles:
                plt.figure(figsize=(17,4))
                pda_arr = []
                db = dbs[percentile]
                for date in date_generated:
                    arr = db[date]
                    zeros = np.count_nonzero(arr==0)
                    pda_i = ((no_cells - zeros) / no_cells) * 100
                    pda_arr.append(pda_i)
                
                plt.plot(date_generated, pda_arr, label='PDA - ' + analysis + ' - Percentile ' + str(percentile))
                        
                locator = mdates.YearLocator()
                fmt = mdates.DateFormatter('%Y')
            
                X = plt.gca().xaxis
                X.set_major_locator(locator)
                X.set_major_formatter(fmt)
                
                plt.ylim(-5, 105)
                
                print_variable = variable.title().replace("_"," ")
                
                plt.legend()
                if len(analysis_names) > 1:
                    title = "Percentage Drought Area (" + print_variable + ") (percentile " + str(percentile) + ")"
                else:
                    title = "Percentage Drought Area (" + print_variable + " - " + analysis + ") (percentile " + str(percentile) + ")"
               
                xlabel = "Year"
                ylabel = "PDA [%]"
                
                plt.title(title, pad=30, fontsize=20)
                plt.xlabel(xlabel, fontdict=None, labelpad=None)
                plt.ylabel(ylabel, fontdict=None, labelpad=None)
            
                if dst_path != None:
                    plt.savefig(dst_path + "Graph_analysis_PDA_perc_" + str(percentile) + "_" + variable + ".pdf", dpi=dpi, bbox_inches='tight')
                
                plt.show
        
def PDASDIGraphing(sdi, intervals, db_path, start_date=None, end_date=None, 
                   separated=0, dst_path=None, dpi=600):
    
    dbs = {}
    
    for interval in intervals:
        with open(db_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[sdi + str(interval)] = db[sdi][sdi + str(interval)][sdi + str(interval) + "_State"]
    
    if start_date == None and end_date == None:
        start = db['start']
        end = db['end']
        db = None
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
            
    date_generated = pd.to_datetime(pd.date_range(str(start.strftime("%Y-%m-%d")),str(end.strftime("%Y-%m-%d")), freq='MS'))
    date_generated = [date_generated[i].date() for i in range(len(date_generated))]
    
    no_cells = np.count_nonzero(~np.isnan(dbs[sdi + str(intervals[0])][:,:,0]))
    
    if separated == 0:
        plt.figure(figsize=(17,4))
        for interval in intervals:
            pda_arr = []
            db = dbs[sdi + str(interval)]
            for c in range(len(date_generated)):
                arr = db[:,:,c]
                zeros = np.count_nonzero(arr==0)
                pda_i = ((no_cells - zeros) / no_cells) * 100
                pda_arr.append(pda_i)
            
            plt.plot(date_generated, pda_arr, label='PDA - ' + sdi + str(interval))
                
        locator = mdates.YearLocator()
        fmt = mdates.DateFormatter('%Y')
    
        X = plt.gca().xaxis
        X.set_major_locator(locator)
        X.set_major_formatter(fmt)
        
        plt.ylim(-5, 105)
                
        plt.legend()
        title = "Percentage Drought Area (" + sdi + str(interval) + ")"
       
        xlabel = "Year"
        ylabel = "PDA [%]"
        
        plt.title(title, pad=30, fontsize=20)
        plt.xlabel(xlabel, fontdict=None, labelpad=None)
        plt.ylabel(ylabel, fontdict=None, labelpad=None)
    
        if dst_path != None:
            plt.savefig(dst_path + "Graph_analysis_PDA_" + sdi + str(interval) + ".pdf", dpi=dpi, bbox_inches='tight')
        
        plt.show
    
    if separated == 1:
        for interval in intervals:
            plt.figure(figsize=(17,4))
            pda_arr = []
            db = dbs[sdi + str(interval)]
            for c in range(len(date_generated)):
                arr = db[:,:,c]
                zeros = np.count_nonzero(arr==0)
                pda_i = ((no_cells - zeros) / no_cells) * 100
                pda_arr.append(pda_i)
            
            plt.plot(date_generated, pda_arr, label='PDA - ' + sdi + str(interval))
                    
            locator = mdates.YearLocator()
            fmt = mdates.DateFormatter('%Y')
        
            X = plt.gca().xaxis
            X.set_major_locator(locator)
            X.set_major_formatter(fmt)
            
            plt.ylim(-5, 105)
                        
            plt.legend()
            title = "Percentage Drought Area (" + sdi + str(interval) + ")"
           
            xlabel = "Year"
            ylabel = "PDA [%]"
            
            plt.title(title, pad=30, fontsize=20)
            plt.xlabel(xlabel, fontdict=None, labelpad=None)
            plt.ylabel(ylabel, fontdict=None, labelpad=None)
            
          
            if dst_path != None:
                plt.savefig(dst_path + "Graph_analysis_PDA_" + sdi + str(interval) + ".pdf", dpi=dpi, bbox_inches='tight')
            
            plt.show

def PDAThermalFloorsGraphing(variable, percentile, dbs_path, identifier, analysis_names, start_date=None, end_date=None, 
                             respect_to=0, separated=0, dst_path=None, dpi=600):
    
    dbs = {}
        
    for analysis, db_path in zip(analysis_names, dbs_path):
        with open(db_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[analysis] = db
        db = None
    
    if start_date == None and end_date == None:
        start = min(dbs[analysis_names[0]]['data'].keys())
        end = max(dbs[analysis_names[0]]['data'].keys())
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
            
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
        
    
    rand_key = random.choice(list(dbs[analysis_names[0]]['data'][start].keys()))
    no_rows = dbs[analysis_names[0]]['data'][start][rand_key].shape[0]
    no_columns = dbs[analysis_names[0]]['data'][start][rand_key].shape[1]
    
    cells_soil_type = np.full((no_rows, no_columns), np.nan)
    
    if separated == 0:
        plt.figure(figsize=(17,4))

    if respect_to == 0:
        no_cells = np.count_nonzero(~np.isnan(dbs[analysis_names[0]]['data'][start][rand_key]))
        mask = ~np.isnan(dbs[analysis_names[0]]['data'][start][rand_key])
        cells_soil_type[mask] = 1

    for analysis in analysis_names:
        db = dbs[analysis]
        for soil_type in db['data'][start].keys():
            pda_arr = []
            if respect_to == 1:
                cells_soil_type = np.full((no_rows, no_columns), np.nan)
                no_cells = np.count_nonzero(db['mask_' + soil_type] == 1)
                mask = db['mask_' + soil_type] == 1
                cells_soil_type[mask] = 1
                        
            for date in date_generated:
                arr = db['data'][date][soil_type]
                zeros = np.count_nonzero((arr * cells_soil_type)==0)
                pda_i = ((no_cells - zeros) / no_cells) * 100
                pda_arr.append(pda_i)
            
            if separated == 0:
                plt.plot(date_generated, pda_arr, label='PDA - ' + analysis + '/' + soil_type)
            
            if separated == 1:
                plt.figure(figsize=(17,4))
                plt.plot(date_generated, pda_arr, label='PDA - ' + analysis + '/' + soil_type)
    
                locator = mdates.YearLocator()
                fmt = mdates.DateFormatter('%Y')
            
                X = plt.gca().xaxis
                X.set_major_locator(locator)
                X.set_major_formatter(fmt)
                
                plt.ylim(-5, 105)
                
                print_variable = variable.title().replace("_"," ")
                
                plt.legend()
                if respect_to == 0:
                    if len(analysis_names) > 1:
                        title = "PDA against cathment area " + soil_type + " (" + print_variable + ") (percentile " + str(percentile) + ")"
                    else:
                        title = "PDA against cathment area " + soil_type + " (" + print_variable + " - " + analysis + ") (percentile " + str(percentile) + ")"
                else:
                    if len(analysis_names) > 1:
                        title = "Percentage Drought Area " + soil_type + " (" + print_variable + ") (percentile " + str(percentile) + ")"
                    else:
                        title = "Percentage Drought Area " + soil_type + " (" + print_variable + " - " + analysis + ") (percentile " + str(percentile) + ")"
                
                xlabel = "Year"
                ylabel = "PDA [%]"
                
                print([sum(pda_arr), soil_type])
                
                plt.title(title, pad=30, fontsize=20)
                plt.xlabel(xlabel, fontdict=None, labelpad=None)
                plt.ylabel(ylabel, fontdict=None, labelpad=None)
            
                if dst_path != None:
                    if respect_to == 0:
                        plt.savefig(dst_path + "Graph_analysis_PDA_perc_" + str(percentile) + "_" + soil_type.replace(" ","_") + "_total_" + variable + ".pdf", dpi=dpi, bbox_inches='tight')
                    else:
                        plt.savefig(dst_path + "Graph_analysis_PDA_perc_" + str(percentile) + "_" + soil_type.replace(" ","_") + "_" + variable + ".pdf", dpi=dpi, bbox_inches='tight')
               
                plt.show
                # plt.close()
        
        if separated == 0:
            locator = mdates.YearLocator()
            fmt = mdates.DateFormatter('%Y')
        
            X = plt.gca().xaxis
            X.set_major_locator(locator)
            X.set_major_formatter(fmt)
            
            plt.ylim(-5, 105)
            
            print_variable = variable.title().replace("_"," ")
            
            plt.legend()
            if respect_to == 0:
                if len(analysis_names) > 1:
                    title = "Percentage Drought Area against cathment area (" + print_variable + ") (percentile " + str(percentile) + ")"
                else:
                    title = "Percentage Drought Area against cathment area (" + print_variable + " - " + analysis + ") (percentile " + str(percentile) + ")"
            else:
                if len(analysis_names) > 1:
                    title = "Percentage Drought Area against " + identifier.replace("_"," ") + " area (" + print_variable + ") (percentile " + str(percentile) + ")"
                else:
                    title = "Percentage Drought Area against " + identifier.replace("_"," ") + " area (" + print_variable + " - " + analysis + ") (percentile " + str(percentile) + ")"
            
            xlabel = "Year"
            ylabel = "PDA [%]"
            
            plt.title(title, pad=30, fontsize=20)
            plt.xlabel(xlabel, fontdict=None, labelpad=None)
            plt.ylabel(ylabel, fontdict=None, labelpad=None)
        
            if dst_path != None:
                if respect_to == 0:
                    plt.savefig(dst_path + "Graph_analysis_PDA_specific_total_" + identifier + "_perc_" + str(percentile) + "_" + variable + ".pdf", dpi=dpi, bbox_inches='tight')
                else:
                    plt.savefig(dst_path + "Graph_analysis_PDA_specific_" + identifier + "_perc_" + str(percentile) + "_" + variable + ".pdf", dpi=dpi, bbox_inches='tight')
           
            plt.show
            # plt.close()
                
def NCDAVsCDAGraphing(variable, percentile, analyses, db_files, reference_raster, 
                      start_date=None, end_date=None, dst_path=None, dpi=600):
    
    dbs = {}
    
    for db_file, analysis in zip(db_files, analyses):            
        with open(db_file, 'rb') as handle:
            db = pickle.load(handle)
        dbs[analysis] = db
        db_file = None
    
    if start_date == None and end_date == None:
        start = min(dbs[analysis[0]].keys())
        end = max(dbs[analysis[0]].keys())
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
    
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(7,7))
    ims = []
    for date in date_generated:
        inner_arr = []
        for analysis, ax in zip(analyses, [ax1, ax2]):
            if analysis == 'NCDA':
                im = ax.imshow(dbs[analysis][date], interpolation=None, cmap = colors.ListedColormap(['C0', 'C3']))
            else:
                db_arr = np.array(db[date]['data'], dtype=np.float64)
                db_arr[arr == noval] = np.nan
                im = ax.imshow(db_arr, interpolation=None)  
                textstr = "Number of clusters: " + str(np.nanmax(db_arr).astype(int)) + "."
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                text_num_clusters = ax.text(0.3, 0.020, textstr, transform=ax.transAxes, fontsize=10,
                                            verticalalignment='bottom', bbox=props)
            
            title = ax.text(0.5, 1.03, analysis, size=15, 
                            # size=plt.rcParams["axes.titlesize"],
                            ha="center", transform=ax.transAxes, )
            text_date = plt.text(0.81, 0.06, date.strftime("%d/%m/%Y"),
                                 transform=fig.transFigure)
            inner_arr.append(im)
            inner_arr.append(title)
            inner_arr.append(text_date)
        inner_arr.append(text_num_clusters)
        
        ims.append(inner_arr)
    
        red_patch = mpatches.Patch(color='C3', label='Drought')
        blue_patch = mpatches.Patch(color='C0', label='No Drought')
        ax1.legend(handles=[blue_patch, red_patch], loc = 'upper center', ncol=2,
                  bbox_to_anchor=(0.5,-0.05))
    
    fig.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.subplots_adjust(bottom=0.13)
    plt.suptitle(variable.title().replace("_", " "), fontweight ="bold", size=20, y=0.95)
    
    ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True, repeat_delay=1000)
    print_start = start.strftime("%d_%m_%Y")
    print_end = end.strftime("%d_%m_%Y")
    ani.save(dst_path + "Animation_NCDA_CDA_" + variable + "_perc" + str(percentile) + "_" + print_start + "_to_" + print_end + ".mp4", dpi=dpi)
    
def NCDAVsCDASingleGraphing(variable, percentile, analyses, db_files, reference_raster, 
                            start_date=None, end_date=None, dst_path=None, dpi=600):
    
    dbs = {}
    
    for db_file, analysis in zip(db_files, analyses):            
        with open(db_file, 'rb') as handle:
            db = pickle.load(handle)
        dbs[analysis] = db
        db_file = None
    
    if start_date == None and end_date == None:
        start = min(dbs[analysis[0]].keys())
        end = max(dbs[analysis[0]].keys())
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
    
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
 
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    
    for date in date_generated:
        fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(7,7))
        ax_list = fig.axes
        ims = []
        inner_arr = []
        for analysis, ax in zip(analyses, [ax1, ax2]):
            if analysis == 'CDA':
                db_arr = np.array(db[date]['data'], dtype=np.float64)
                db_arr[arr == noval] = np.nan
                im = ax.imshow(db_arr, interpolation=None)  
                textstr = "Number of clusters: " + str(np.nanmax(db_arr).astype(int)) + "."
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                ax_list[1].text(0.3, 0.020, textstr, transform=ax.transAxes, fontsize=10,
                                verticalalignment='bottom', bbox=props)
                
            else:
                im = ax.imshow(dbs[analysis][date], interpolation=None, cmap = colors.ListedColormap(['C0', 'C3']))
                red_patch = mpatches.Patch(color='C3', label='Drought')
                blue_patch = mpatches.Patch(color='C0', label='No Drought')
                ax.legend(handles=[blue_patch, red_patch], loc = 'upper center', ncol=2,
                          bbox_to_anchor=(0.5,-0.05))
            title = ax.text(0.5, 1.03, analysis, size=15, 
                            # size=plt.rcParams["axes.titlesize"],
                            ha="center", transform=ax.transAxes, )
            text_date = plt.text(0.81, 0.06, date.strftime("%d/%m/%Y"),
                                 transform=fig.transFigure)
            inner_arr.append(im)
            inner_arr.append(title)
            inner_arr.append(text_date)
    
        ims.append(inner_arr)
    
        fig.tight_layout()
        plt.subplots_adjust(top=0.85)
        plt.subplots_adjust(bottom=0.13)
        plt.suptitle(variable.title().replace("_", " "), fontweight ="bold", size=20, y=0.95)
        print_date = date.strftime("%d_%m_%Y")
        
        if dst_path != None:
            plt.savefig(dst_path + "Graph _NCDA_CDA_" + variable + "_perc" + str(percentile) + "_" + print_date + ".pdf", dpi=dpi, bbox_inches='tight')
        
        plt.show()                

def DroughtEventsNumberSDIGraphing(sdi_names, intervals, db_files, row, column, 
                                   dst_path=None, dpi=600):
    
    dbs = {}
    
    for sdi, db_file in zip(sdi_names, db_files):
        with open(db_file, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[sdi] = db
        db = None

    stats = ['No_events',
              'Magnitude_mean',
              'Magnitude_standard_deviation', 
              'Magnitude_max',
              'Magnitude_min',
              'Duration_mean',
              'Duration_standard_deviation',
              'Duration_max',
              'Duration_min'
             ]
    
    for stat in stats:
        data = {}
        for sdi in list(dbs.keys()):
            value_array = []
            for i in intervals:
                interval_key = sdi + str(i)
                stats_key = interval_key + '_Stats'
                value_array.append(dbs[sdi][sdi][interval_key][stats_key][row, column][stat])
                
            data[sdi] = value_array
    
        total_width = 0.8
        single_width = 0.8
        
        fig, ax = plt.subplots()
        ax.set_xticks(np.asarray([i for i in range(len(value_array))]))
        ax.set_xticklabels(intervals)
        
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        n_bars = len(data)
    
        # The width of a single bar
        bar_width = total_width / n_bars
    
        # List containing handles for the drawn bars, used for the legend
        bars = []
    
        # Iterate over all data
        for i, (name, values) in enumerate(data.items()):
            # The offset in x direction of that bar
            x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
    
            # Draw a bar for every value of that type
            for x, y in enumerate(values):
                bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])
    
            # Add a handle to the last drawn bar, which we'll need for the legend
            bars.append(bar[0])
    
        ax.legend(bars, data.keys())
        
        ax.set_title(stat.title().replace("_", " ") + " in cell r" + str(row) + "c" + str(column))
            
        fig.tight_layout()
        
        if dst_path != None:
            plt.savefig(dst_path + "Graph_analysis_SDI_bar_chart_comparisson_" + stat + "_r" + str(row) + "_c" + str(column) + ".pdf", dpi=dpi, bbox_inches='tight')
        
        plt.show()            
    
def PDAMultiplePercentileGraphing(variable, percentiles, dbs_path, analysis_names, start_date=None, end_date=None,
                                  dst_path=None, dpi=600):
    
    dbs = {}
        
    for analysis, db_path in zip(analysis_names, dbs_path):
        with open(db_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[analysis] = db
        db = None
    
    if start_date == None and end_date == None:
        start = min(dbs[analysis_names[0]].keys())
        end = max(dbs[analysis_names[0]].keys())
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
            
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    plt.figure(figsize=(5,5))
    no_cells = np.count_nonzero(~np.isnan(dbs[analysis_names[0]][start]))
    
    for analysis in analysis_names:
        pda_arr = []
        areas = []
        db = dbs[analysis]
        for percentile in percentiles:
            for date in date_generated:
                arr = db[date]
                zeros = np.count_nonzero(arr==0)
                pda_i = (no_cells - zeros) * 25
                pda_arr.append(pda_i)
        
            areas.append(np.trapz(pda_arr))
            # areas.append(sum(pda_arr))
            
        plt.plot(percentiles, areas, label='Accumulated DA - ' + analysis, color='C0', marker='.')
        # print(variable, percentiles, areas)
    print_variable = variable.title().replace("_"," ")
    
    plt.legend()
    if len(analysis_names) > 1:
        title = "Accumulated Drought Area (" + print_variable + ")"
    else:
        title = "Accumulated Drought Area (" + print_variable + " - " + analysis + ")"
   
    xlabel = "Percentile"
    ylabel = "Accumulated DA [km^2]"
    
    plt.title(title, pad=30, fontsize=20)
    plt.xlabel(xlabel, fontdict=None, labelpad=None)
    plt.ylabel(ylabel, fontdict=None, labelpad=None)

    if dst_path != None:
        plt.savefig(dst_path + "Graph_analysis_accum_DA_" + variable + ".pdf", dpi=dpi, bbox_inches='tight')
    
    plt.show

def CorrMatrixGraphing(sdi_names, intervals, db_files, dst_path=None, dpi=600):
    
    dbs = {}
        
    for sdi, db_path in zip(sdi_names, db_files):
        with open(db_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[sdi] = db
        db = None
        
    stats = ['No_events',
             'Magnitude_mean',
             'Magnitude_standard_deviation', 
             'Magnitude_max',
             'Magnitude_min',
             'Duration_mean',
             'Duration_standard_deviation',
             'Duration_max',
             'Duration_min']
    
    no_rows = dbs[sdi_names[0]][sdi_names[0]][sdi_names[0] + str(intervals[0])][sdi_names[0] + str(intervals[0]) + '_Stats'].shape[0]
    no_columns = dbs[sdi_names[0]][sdi_names[0]][sdi_names[0] + str(intervals[0])][sdi_names[0] + str(intervals[0]) + '_Stats'].shape[1]
    
    comb = []
    
    for sdi in sdi_names:
        for interval in intervals:
            comb.append(sdi + str(interval))   
    
    for stat in stats:
        df = pd.DataFrame()
        for sdi in sdi_names:
            for interval in intervals:
                clean_arr = np.full((no_rows, no_columns), np.nan)
                for row in range(no_rows):
                    for column in range(no_columns):
                        if pd.isnull(np.array(dbs[sdi][sdi][sdi + str(interval)][sdi + str(interval) + '_Stats'][row, column], dtype=object)):
                            continue
                        clean_arr[row, column] = dbs[sdi][sdi][sdi + str(interval)][sdi + str(interval) + '_Stats'][row, column][stat]
                
                clean_arr = clean_arr[~np.isnan(clean_arr)]
                df[sdi + str(interval)] = clean_arr.flatten()
                
        corr_mat = df.corr()
                
        fig, ax = plt.subplots(figsize=(10, 10))
        # Using matshow here just because it sets the ticks up nicely. imshow is faster.
        im = ax.matshow(corr_mat)
        
        for (i, j), z in np.ndenumerate(corr_mat):
            ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
                        
        # # We want to show all ticks...
        ax.set_xticks(np.arange(len(sdi_names) * len(intervals)))
        ax.set_yticks(np.arange(len(sdi_names) * len(intervals)))
        # # ... and label them with the respective list entries
        ax.set_xticklabels(comb, fontsize=16)
        ax.set_yticklabels(comb, fontsize=16)
        
        ax.tick_params(top=True, bottom=False,
            labeltop=True, labelbottom=False)
        
        # # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left",
                  rotation_mode="anchor")
                
        ax.set_title(stat.replace('_', ' '), fontsize=30)
        
        cbar = fig.colorbar(im)
        cbar.ax.tick_params(labelsize=18)
        
        if dst_path != None:
            plt.savefig(dst_path + "Graph_analysis_Correlation_Matrix_" + stat + ".pdf", dpi=dpi, bbox_inches='tight')

        plt.show()
                
def ColorMeshPDASDIGraphing(sdi, intervals, db_path, start_date=None, end_date=None, 
                            dst_path=None, dpi=600):
        
    dbs = {}
    
    for interval in intervals:
        with open(db_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[sdi + str(interval)] = db[sdi][sdi + str(interval)][sdi + str(interval) + "_State"]
    
    if start_date == None and end_date == None:
        start = db['start']
        end = db['end']
        db = None
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
            
    date_generated = pd.to_datetime(pd.date_range(str(start.strftime("%Y-%m-%d")),str(end.strftime("%Y-%m-%d")), freq='MS'))
    date_generated = [date_generated[i].date() for i in range(len(date_generated))]
    months = [i for i in range(12)]
    years = [date_generated[i].year for i in range(len(date_generated))]
    years = list(dict.fromkeys(years))
    
    no_cells = np.count_nonzero(~np.isnan(dbs[sdi + str(intervals[0])][:,:,0]))
            
    for interval in intervals:
        plt.figure(figsize=(17,4))
        db = dbs[sdi + str(interval)]
        df = pd.DataFrame()
        c = 0
        for year in years:
            pda_arr = []
            for month in months:
                arr = db[:,:,c]
                zeros = np.count_nonzero(arr==0)
                pda_i = ((no_cells - zeros) / no_cells) * 100
                pda_arr.append(pda_i)
                c += 1
            df[year] = pda_arr
        df.index = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        plt.pcolormesh(df)
        plt.clim(0, 100)
        plt.colorbar(pad=0.01)
        
        plt.set_cmap('hot_r')
        plt.xticks(np.arange(len(years))+ 0.5, years)
        plt.yticks(np.arange(len(df.index.tolist())) + 0.5, df.index.tolist())
        
        plt.xlabel('Year', fontdict=None, labelpad=None)
        plt.ylabel('Month', fontdict=None, labelpad=None)
        plt.title('PDA - ' + sdi + str(interval), pad=30, fontsize=20)
        
        if dst_path != None:
            plt.savefig(dst_path + "Graph_analysis_PDA_mesh_" + sdi + str(interval) + ".pdf", dpi=dpi, bbox_inches='tight')
    
        plt.show()

def ColorMeshPDAGraphing(variable, percentile, db_path, analysis, start_date=None, end_date=None, 
                         dst_path=None, dpi=600):
        
    with open(db_path, 'rb') as handle:
        db = pickle.load(handle) 
    
    if start_date == None and end_date == None:
        start = min(db.keys())
        end = max(db.keys())
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
            
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    years = [date_generated[i].year for i in range(len(date_generated))]
    years = list(dict.fromkeys(years))

    no_cells = np.count_nonzero(~np.isnan(db[start]))    
    
    plt.figure(figsize=(17,4))
    pda_arr = []
    df = pd.DataFrame()
    year = date_generated[0].year
    for date in date_generated:
        arr = db[date]
        zeros = np.count_nonzero(arr==0)
        pda_i = ((no_cells - zeros) / no_cells) * 100
        pda_arr.append(pda_i)
        if date.year != (date + timedelta(days=1)).year:
            if len(pda_arr) == 365:
                pda_arr.append(np.nan)
            df[year] = pda_arr
            pda_arr = []
            year += 1
    
    plt.pcolormesh(df.T)
    plt.clim(0, 100)
    plt.colorbar(pad=0.01)
    
    plt.set_cmap('hot_r')
    # plt.xticks(np.arange(len(df.index.tolist())) + 0.5, df.index.tolist())
    plt.yticks(np.arange(len(years))+ 0.5, years)
    
    plt.xlabel('Day', fontdict=None, labelpad=None)
    plt.ylabel('Year', fontdict=None, labelpad=None)
    plt.title('PDA - ' + analysis + ' ' + variable.capitalize().replace('_', ' ') + ' (percentile ' + str(percentile) + ')', pad=30, fontsize=20)
    
    if dst_path != None:
        plt.savefig(dst_path + "Graph_analysis_PDA_mesh_" + analysis + "_" + variable + "_perc_" + str(percentile) + ".pdf", dpi=dpi, bbox_inches='tight')

    plt.show()

def ComparisonPDANCDASDIGraphing(variable, percentiles, dbs_path, analysis, sdi, intervals, sdi_db_path,
                                 start_date=None, end_date=None, separated=0, dst_path=None, dpi=600):
    
    dbs = {}
    
    for db_path, percentile in zip(dbs_path, percentiles):
        with open(db_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[percentile] = db
        db = None
    
    if start_date == None and end_date == None:
        start = min(dbs[percentiles[0]].keys())
        end = max(dbs[percentiles[0]].keys())
    else:
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
            
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    no_cells = np.count_nonzero(~np.isnan(dbs[percentiles[0]][start]))
            
    for interval in intervals:
        with open(sdi_db_path, 'rb') as handle:
            db = pickle.load(handle) 
        dbs[sdi + str(interval)] = db[sdi][sdi + str(interval)][sdi + str(interval) + "_State"]
        db = None
                
    date_generated_sdi = pd.to_datetime(pd.date_range(str(start.strftime("%Y-%m-%d")),str(end.strftime("%Y-%m-%d")), freq='MS'))
    date_generated_sdi = [date_generated_sdi[i].date() for i in range(len(date_generated_sdi))]
        
    for interval in intervals:
        for percentile in percentiles:
            plt.figure(figsize=(17,4))
            pda_arr = []
            pda_arr_sdi = []
            db = dbs[percentile]
            db_sdi = dbs[sdi + str(interval)]
            
            for c in range(len(date_generated_sdi)):
                arr_sdi = db_sdi[:,:,c]
                zeros_sdi = np.count_nonzero(arr_sdi==0)
                pda_i_sdi = ((no_cells - zeros_sdi) / no_cells) * 100
                pda_arr_sdi.append(pda_i_sdi)
            
            for date in date_generated:
                arr = db[date]
                zeros = np.count_nonzero(arr==0)
                pda_i = ((no_cells - zeros) / no_cells) * 100
                pda_arr.append(pda_i)
            
            date_arr_sdi = []
            c = 0
            for date in date_generated:
                if date.day == 1:
                    date_arr_sdi.append(c)
                c += 1
            
            
            pda_arr_sdi = np.interp(np.arange(0, len(date_generated)), date_arr_sdi, pda_arr_sdi)
            plt.plot(date_generated, pda_arr_sdi, label='PDA - ' + sdi + str(interval))
            plt.plot(date_generated, pda_arr, label='PDA - ' + analysis + ' - Percentile ' + str(percentile))
            
            corr_pearson = scistat.pearsonr(pda_arr, pda_arr_sdi)[0]
            corr_spearman = scistat.spearmanr(pda_arr, pda_arr_sdi)[0]
            corr_kendall = scistat.kendalltau(pda_arr, pda_arr_sdi)[0]
            # np.corrcoef(pda_arr, pda_arr_sdi)[0, 1]
            # corr_
            
            locator = mdates.YearLocator()
            fmt = mdates.DateFormatter('%Y')
        
            X = plt.gca().xaxis
            X.set_major_locator(locator)
            X.set_major_formatter(fmt)
            
            plt.ylim(-5, 105)
            
            print_variable = variable.title().replace("_"," ")
            
            plt.legend()
            title = "Percentage Drought Area (" + print_variable + " - percentile " + str(percentile) + ") vs. " + sdi + str(interval)
           
            xlabel = "Year"
            ylabel = "PDA [%]"
            
            plt.title(title, pad=30, fontsize=20)
            plt.xlabel(xlabel, fontdict=None, labelpad=None)
            plt.ylabel(ylabel, fontdict=None, labelpad=None)
            
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            
            corr_text = "Pearson's r = " + str(round(corr_pearson, 4)) + ", Spearman's rho = " + str(round(corr_spearman, 4)) + ", Kendall's tau = " + str(round(corr_kendall, 4))
            
            plt.annotate(corr_text, xy=(0, 1.15), xytext=(12, -12), va='top',
                         xycoords='axes fraction', textcoords='offset points', bbox=props)
            
            # plt.text(1, 1, "Pearson's r = " + str(round(corr_r, 4)), fontsize=14,
            #          verticalalignment='top', bbox=props)
        
            if dst_path != None:
                plt.savefig(dst_path + "Graph_analysis_PDA_comparison_" + variable + "_perc" + str(percentile) + "_" + sdi + str(interval) + ".pdf", dpi=dpi, bbox_inches='tight')
            
            plt.show

def NumberOfClustersGraphing(variable, percentile, db_file, start_date=None, end_date=None, dst_path=None, dpi=600):
    
    with open(db_file, 'rb') as handle:
        db = pickle.load(handle)
    
    start = min(db.keys())
    end = max(db.keys())    
    
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    num_events = []
    
    for date in date_generated:
        num = db[date]['Number_of_clusters']
        num_events.append(num)
     
    plt.figure(figsize=(17,4))
    
    x = date_generated
    # plt.plot(x, num_events)
    plt.bar(x, num_events)
    
    locator = mdates.YearLocator()
    fmt = mdates.DateFormatter('%Y')

    X = plt.gca().xaxis
    X.set_major_locator(locator)
    X.set_major_formatter(fmt)
    
    # y_max = max(num_events)
    # import math
    # y_max_lim = 10 * math.ceil(y_max/10)
    # y_min_lim = (y_max_lim - y_max)
    
    # plt.ylim(-y_min_lim, y_max_lim)
    
    # yint = range(-y_min_lim, y_max_lim)
    # plt.yticks(yint)
    
    from matplotlib.ticker import MaxNLocator
    
    Y = plt.gca().yaxis
    Y.set_major_locator(MaxNLocator(integer=True))    
    
    print_variable = variable.title().replace("_"," ")
    
    # plt.legend()
    title = "Drought Clusters (" + print_variable + ") (percentile " + str(percentile) + ")"
    
    xlabel = "Year"
    ylabel = "Number of Drought Clusters"
    
    plt.title(title, pad=30, fontsize=20)
    plt.xlabel(xlabel, fontdict=None, labelpad=None)
    plt.ylabel(ylabel, fontdict=None, labelpad=None)

    if dst_path != None:
        plt.savefig(dst_path + "Graph_analysis_Number_of_drought_clusters_" + variable + "_perc" + str(percentile) + ".pdf", dpi=dpi, bbox_inches='tight')
    
    plt.show

def RasterStatsGraphing(main_path, sdi_names, intervals, stat, reference_raster, 
                        dst_path=None, dpi=600):
    
    sdi_list = []
    stat_paths = []
    stat_arrays = {}
    stat_names = []
    stat_keys = []
    
    for sdi in sdi_names:
        for interval in intervals:
            sdi_list.append(sdi + str(interval))
            stat_names.append((sdi + str(interval) + "_" + stat).capitalize().replace("_", " "))
            stat_keys.append(sdi + str(interval) + "_" + stat)
            stat_paths.append(main_path + "/Datos/SDI/" + sdi + "/stats/" + sdi + str(interval) + "_" + stat + ".tif")
            for stat_path in stat_paths:
                stat_raster = gdal.Open(stat_path)
                stat_arrays[sdi + str(interval) + "_" + stat] = stat_raster.GetRasterBand(1).ReadAsArray()
                stat_raster.FlushCache()
                stat_raster = None
        
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    raster.FlushCache()
    raster = None
    
    i = 0
    for stat_key in stat_keys:
        if i == 0:
            min_value = np.nanmin(stat_arrays[stat_key])
            max_value = np.nanmax(stat_arrays[stat_key])
        if min_value < np.nanmin(stat_arrays[stat_key]):
            min_value = np.nanmin(stat_arrays[stat_key])
        if max_value < np.nanmax(stat_arrays[stat_key]):
            max_value = np.nanmax(stat_arrays[stat_key])
        i += 1
        
    Tot = len(stat_keys)
    Cols = len(stat_keys)
    
    Rows = Tot // Cols 
    Rows += Tot % Cols
        
    Position = range(1,Tot + 1)
    
    ims = []
    inner_arr = []
    fig = plt.figure(1, figsize=(17,4))
    k = 0
    for stat_key, sdi in zip(stat_keys, sdi_list):
        
        ax = fig.add_subplot(Rows,Cols,Position[k])
        stat_arrays[stat_key][arr == noval] = np.nan
            
        im = ax.imshow(stat_arrays[stat_key], interpolation=None, 
                       vmin=0, vmax=max_value, cmap=plt.get_cmap('YlOrRd'))
        title = ax.text(0.5, 1.03, sdi, size=15, 
                        # size=plt.rcParams["axes.titlesize"],
                        ha="center", transform=ax.transAxes, )
        
        if k != 0:
            plt.yticks([])

        inner_arr.append(im)
        inner_arr.append(title)
        
        k += 1
    
    ims.append(inner_arr)

    plt.subplots_adjust(top=0.85)
    
    plt.legend
    plt.subplots_adjust(bottom=0.0000001)

    ax_list = fig.axes
    
    fig.colorbar(im, ax=ax_list, orientation='horizontal', 
                 panchor = (0,0), aspect = 80, shrink = 1)
    
    plt.suptitle(stat.title().replace("_", " "), fontweight ="bold", size=20, y=1)
    
    if dst_path != None:
        plt.savefig(dst_path + "Graph_analysis_DI_Comparison_" + stat + ".pdf", dpi=dpi, bbox_inches='tight')

    plt.show()

def RasterHorizontalGraphing(sdi, interval, db_path, date_range, reference_raster, 
                             colorbar=True, dst_path=None, dpi=600):
    
    with open(db_path, 'rb') as handle:
        db = pickle.load(handle)
    
    start = db['start']
    end = db['end']
    
    initial = datetime.strptime(date_range[0], '%d/%m/%Y')
    final = datetime.strptime(date_range[1], '%d/%m/%Y')
        
    num_months = (initial.year - start.year) * 12 + (initial.month - start.month)
    
    date_generated = pd.to_datetime(pd.date_range(str(initial.strftime("%Y-%m-%d")),str(final.strftime("%Y-%m-%d")), freq='MS'))
    date_generated = [date_generated[i].date() for i in range(len(date_generated))]
    
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    raster.FlushCache()
    raster = None
           
    Tot = len(date_generated)
    Cols = len(date_generated)
    
    Rows = Tot // Cols 
    Rows += Tot % Cols
        
    Position = range(1,Tot + 1)
    
    ims = []
    inner_arr = []
    fig = plt.figure(1, figsize=(17,4))
    k = 0
    for date, c in zip(date_generated, range(num_months, num_months + len(date_generated))):
        ax = fig.add_subplot(Rows,Cols,Position[k])
        db[sdi][sdi + str(interval)][:,:,c][arr == noval] = np.nan
            
        im = ax.imshow(db[sdi][sdi + str(interval)][:,:,c], interpolation=None, 
                       vmin=0-0.5, vmax=6+0.5, cmap=plt.get_cmap('YlOrRd_r', 6+1))
        title = ax.text(0.5, 1.03, str(date.month) + "/" + str(date.year), size=8, 
                        # size=plt.rcParams["axes.titlesize"],
                        ha="center", transform=ax.transAxes, )
        
        if k != 0:
            plt.yticks([])

        inner_arr.append(im)
        inner_arr.append(title)
        
        k += 1
    
    ims.append(inner_arr)

    plt.subplots_adjust(top=0.9)
    
    # plt.legend
    plt.subplots_adjust(bottom=0.0000001)
    
    ax_list = fig.axes
    fig.colorbar(im, ax=ax_list, orientation='horizontal', ticks=np.arange(0, 7),
                 panchor = (0,0), aspect = 80, shrink = 1)
    
    sup_title = "Development of drought according to " +  sdi + str(interval) + " in the monthly period from " + date_range[0] + " to " + date_range[1]
    
    plt.suptitle(sup_title , size=20, y=0.8)
    
    if dst_path != None:
        plt.savefig(dst_path + "Graph_analysis_" + sdi + str(interval) + "_classes_" + date_range[0].replace('/', '_') + "_" + date_range[1].replace('/', '_') + ".pdf", dpi=dpi, bbox_inches='tight')

    plt.show()

def SDIClassesAnimation(sdi, interval, db_path, reference_raster, colorbar=True,
                        start_date=None, end_date=None, dst_path=None, dpi=600):
        
    with open(db_path, 'rb') as handle:
        db = pickle.load(handle)
    
    start = db['start']
    end = db['end']
    
    initial = datetime.strptime(start_date, "%d-%m-%Y")
    final = datetime.strptime(end_date, "%d-%m-%Y")
    num_months = (initial.year - start.year) * 12 + (initial.month - start.month)
    
    date_generated = pd.to_datetime(pd.date_range(str(initial.strftime("%Y-%m-%d")),str(final.strftime("%Y-%m-%d")), freq='MS'))
    date_generated = [date_generated[i].date() for i in range(len(date_generated))]
    
    raster = gdal.Open(reference_raster)
    arr = raster.GetRasterBand(1).ReadAsArray()
    noval = raster.GetRasterBand(1).GetNoDataValue()
    
    fig, ax = plt.subplots(figsize=(5,7))
    ims = []
        
    inner_arr = []
    for date, c in zip(date_generated, range(num_months, num_months + len(date_generated))):
        inner_arr=[]
        db[sdi][sdi + str(interval)][:,:,c][arr == noval] = np.nan
        
        im = ax.imshow(db[sdi][sdi + str(interval)][:,:,c], interpolation=None, 
                       vmin=0-0.5, vmax=6+0.5, cmap=plt.get_cmap('YlOrRd_r', 6+1))
        title = ax.text(0.5, 1.03, str(date.month) + "/" + str(date.year), size=8, 
                        # size=plt.rcParams["axes.titlesize"],
                        ha="center", transform=ax.transAxes, )
        
        inner_arr.append(im)
        inner_arr.append(title)        
    
        ims.append(inner_arr)

    fig.tight_layout()   
    plt.subplots_adjust(top=0.85)
    
    ax_list = fig.axes
    fig.colorbar(im, ax=ax_list, orientation='vertical', ticks=np.arange(0, 7))
    
    sup_title = "Drought classes - " +  sdi + str(interval)
    plt.suptitle(sup_title, fontweight ="bold", size=20, y=0.95)
    
    ani = animation.ArtistAnimation(fig, ims, interval=400, blit=True, repeat_delay=1000)
    print_start = initial.strftime("%d_%m_%Y")
    print_end = final.strftime("%d_%m_%Y")
    ani.save(dst_path + "Animation_" + sdi + str(interval) + "_classes_" + print_start + "_" + print_end + ".mp4", dpi=dpi)


# def NCDAVariablesComparisonGraphing(variable, percentile, analyses, db_files, reference_raster, 
#                                     start_date=None, end_date=None, dst_path=None, dpi=600):
    
#     dbs = {}
    
#     for db_file, analysis in zip(db_files, analyses):            
#         with open(db_file, 'rb') as handle:
#             db = pickle.load(handle)
#         dbs[analysis] = db
#         db_file = None
    
#     if start_date == None and end_date == None:
#         start = min(dbs[analysis[0]].keys())
#         end = max(dbs[analysis[0]].keys())
#     else:
#         start = datetime.strptime(start_date, "%d-%m-%Y")
#         end = datetime.strptime(end_date, "%d-%m-%Y")
    
#     date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
#     raster = gdal.Open(reference_raster)
#     arr = raster.GetRasterBand(1).ReadAsArray()
#     noval = raster.GetRasterBand(1).GetNoDataValue()
    
#     fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(7,7))
#     ims = []
#     for date in date_generated:
#         inner_arr = []
#         for analysis, ax in zip(analyses, [ax1, ax2]):
#             if analysis == 'CDA':
#                 db_arr = np.array(db[date]['data'], dtype=np.float64)
#                 db_arr[arr == noval] = np.nan
#                 im = ax.imshow(db_arr, interpolation=None)
#                 if date == start:
#                     ax.imshow(db_arr, interpolation=None)  # show an initial one first
#             else:
#                 im = ax.imshow(dbs[analysis][date], interpolation=None, cmap = colors.ListedColormap(['C0', 'C3']))
#                 if date == start:
#                     ax.imshow(dbs[analysis][date], interpolation=None, cmap = colors.ListedColormap(['C0', 'C3']))  # show an initial one first
#             title = ax.text(0.5, 1.03, analysis, size=15, 
#                             # size=plt.rcParams["axes.titlesize"],
#                             ha="center", transform=ax.transAxes, )
#             text_date = plt.text(0.8, 0.05, date.strftime("%d/%m/%Y"),
#                                  transform=fig.transFigure)
#             inner_arr.append(im)
#             inner_arr.append(title)
#             inner_arr.append(text_date)
    
#         ims.append(inner_arr)
    
#     red_patch = mpatches.Patch(color='C3', label='Drought')
#     blue_patch = mpatches.Patch(color='C0', label='No Drought')
    
#     fig.tight_layout()
#     plt.subplots_adjust(top=0.85)
    
#     plt.legend(handles=[blue_patch, red_patch], loc = 'lower center', ncol=2,
#                bbox_to_anchor=(0.5,0.03), bbox_transform=fig.transFigure)
#     plt.subplots_adjust(bottom=0.13)
#     plt.suptitle(variable.title().replace("_", " "), fontweight ="bold", size=20, y=0.95)
    
#     ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True, repeat_delay=1000)
#     print_start = start.strftime("%d_%m_%Y")
#     print_end = end.strftime("%d_%m_%Y")
#     ani.save(dst_path + "Animation_NCDA_CDA_" + variable + "_perc" + percentile + "_" + print_start + "_to_" + print_end + ".mp4", dpi=dpi)

def RunoffVSPrecipitationGraphing(db_file_runoff, db_file_prec, cuencas_path,
                                  rows, columns, cuencas_names, dst_path=None, dpi=600):

    cuencas_ras = gdal.Open(cuencas_path)
    cuencas_arr = cuencas_ras.GetRasterBand(1).ReadAsArray()
    noval = cuencas_ras.GetRasterBand(1).GetNoDataValue()
    [no_rows, no_columns] = cuencas_arr.shape
    
    with open(db_file_runoff, 'rb') as handle:
        db_runoff = pickle.load(handle) 
    with open(db_file_prec, 'rb') as handle:
        db_prec = pickle.load(handle) 
    
    months = [i for i in range(12)]
    
    for row, column, cuenca in zip(rows, columns, cuencas_names):
        
        new_cuenca = np.full((no_rows, no_columns), np.nan)
        if cuenca == 1 or cuenca == 3:
            new_cuenca[cuencas_arr == cuenca] = 1
        elif cuenca == 2:
            new_cuenca[(cuencas_arr == cuenca) | (cuencas_arr == 1)] = 1
        elif cuenca == 4:
            new_cuenca[cuencas_arr != noval] = 1
        
        monthly_value_runoff = []
        monthly_value_prec = []
    
        for month in months:
            monthly_arr_runoff = []
            monthly_arr_prec = []
            months_num_arr = [i for i in range(month, db_runoff['data'].shape[2], 12)]
            for m in months_num_arr:
                monthly_arr_runoff.append(db_runoff['data'][row, column, m])
                zone_mask = new_cuenca == 1
                monthly_arr_prec.append(np.mean(db_prec['data'][:, :, m][zone_mask]))
            
            monthly_value_runoff.append(np.mean(monthly_arr_runoff))
            monthly_value_prec.append(np.mean(monthly_arr_prec))
            
        m1_t = pd.DataFrame({
             'runoff' : monthly_value_runoff,
             'prec' : monthly_value_prec})
        
        fig = plt.figure(figsize=(10,4))
        width = .5 # width of a bar
        
        ax1 = m1_t['runoff'].plot(rot=0, label='Runoff', style='r', zorder=10)    
        ax2 = m1_t['prec'].plot(kind='bar', width = width, secondary_y=True, rot=0,
                                label='Precipitation', zorder=1)
        
        ax1.set_ylabel('Runoff [m3/s]')
        ax1.legend('Runoff')
        ax2.set_ylabel('Precipitation [mm]')
        ax2.legend('Precipitation')
        ax1.set_xlabel('Months')
        
        title = "Runoff Vs. Precipitation in cell r" + str(row) + "c" + str(column)
        plt.title(title, pad=30, fontsize=20)
        
        plt.tight_layout() 
        
        handles,labels = [],[]
        for ax in fig.axes:
            for h,l in zip(*ax.get_legend_handles_labels()):
                handles.append(h)
                labels.append(l)
        
        plt.legend(handles,labels)

        ax = plt.gca()
        plt.xlim([-width, len(m1_t['runoff'])-width])
        ax.set_xticklabels(('J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'))
        
        if dst_path != None:
            plt.savefig(dst_path + "Graph_analysis_runoff_vs_precipitation_in_r" + str(row) + "c" + str(column) + ".pdf", dpi=dpi, bbox_inches='tight')

        plt.show()
