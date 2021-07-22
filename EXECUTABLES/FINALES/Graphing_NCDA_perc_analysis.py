# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 12:23:29 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import ThresholdAnalysisGraphing

variable_units = ["m3/s", "mm/s"]
variables = ["runoff", "soil_moisture"]
percentiles = [60, 65, 70, 75, 80, 85, 90, 95]

main_path = "E:/JC_FA_TESIS/"

year = 2010
row = 108
column = 88
dst_path = main_path + "Datos/Images/"

for variable, variable_unit in zip(variables, variable_units):
    for percentile in percentiles:
        db_path = main_path + "Datos/DBs/model_results/" + variable + "/" + variable + "_daily_db.pickle"
        threshold_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/thresholds/" + variable + "/"
        threshold_series = [threshold_path + "flattened_threshold_monthly_perc_" + str(percentile) + "_leap_year.pickle",
                            threshold_path + "smoothed_threshold_monthly_perc_" + str(percentile) + "_leap_year.pickle",
                            threshold_path + "flattened_threshold_monthly_perc_" + str(percentile) + "_regular_year.pickle",
                            threshold_path + "smoothed_threshold_monthly_perc_" + str(percentile) + "_regular_year.pickle"]
                
        ThresholdAnalysisGraphing(variable,
                                  variable_unit,
                                  percentile,
                                  db_path, 
                                  threshold_series, 
                                  year, 
                                  row, 
                                  column,
                                  dst_path=dst_path)
