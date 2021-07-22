# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 09:55:27 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import PDAMultiplePercentileGraphing

analysis_names = ['NCDA']
variables = ['runoff', 'soil_moisture']
percentiles = [60, 65, 70, 75, 80, 85, 90, 95]

main_path = "E:/JC_FA_TESIS/"

dst_path = main_path + "Datos/Images/"

for variable in variables:
    dbs_path = [main_path + "Datos/DBs/NCDA_CDA/perc_" + str(p) + "/" + analysis_names[0] + "/" + variable + "/drought_binary_" + variable + "_perc_" + str(p) + ".pickle" for p in percentiles]
    PDAMultiplePercentileGraphing(variable, 
                                  percentiles, 
                                  dbs_path, 
                                  analysis_names,
                                  dst_path=dst_path)