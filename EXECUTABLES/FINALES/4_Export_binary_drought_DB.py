# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 04:20:14 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import BinaryDroughtPercentile

variable = 'soil_moisture'
percentile = 85

main_path = "E:/JC_FA_TESIS/"

db_file = main_path + "Datos/DBs/model_results/" + variable + "/" + variable + "_daily_db.pickle"
src_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/thresholds/" + variable + "/"
smoothed_threshold = [src_path + "smoothed_threshold_monthly_perc_" + str(percentile) + "_leap_year.pickle",
                      src_path + "smoothed_threshold_monthly_perc_" + str(percentile) + "_regular_year.pickle"]
output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA/" + variable + "/"

BinaryDroughtPercentile(variable, 
                        percentile, 
                        db_file, 
                        smoothed_threshold, 
                        output_path)



