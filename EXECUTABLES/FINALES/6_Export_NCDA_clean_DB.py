# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 16:57:31 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import CDAAnalysis

variable = 'runoff'
percentile = 90

main_path = "E:/JC_FA_TESIS/"

db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA_raw/" + variable + "/" + "drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA/" + variable + "/"

NCDACleaning(variable, 
             percentile, 
             db_file, 
             output_path)

