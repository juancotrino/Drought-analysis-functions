# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 22:53:13 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import GetThresholdSeries

variable = 'runoff'
percentile = 90

main_path = "E:/JC_FA_TESIS/"

db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/thresholds/" + variable + "/threshold_monthly_" + variable + "_perc_" + str(percentile) + ".pickle"
output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/thresholds/" + variable + "/"
window_length = 45
polyorder = 3

GetThresholdSeries(variable,
                   db_file,
                   percentile, 
                   window_length,
                   polyorder, 
                   output_path)


