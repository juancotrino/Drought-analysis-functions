# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 22:25:25 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import MonthlyPercentile

variable = 'water_stress'
percentile = 85

main_path = "E:/JC_FA_TESIS/"

db_file = main_path + "Datos/DBs/model_results/" + variable + "/" + variable + "_daily_db.pickle"
output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/thresholds/" + variable + "/"

MonthlyPercentile(db_file, 
                  percentile, 
                  variable, 
                  output_path)

