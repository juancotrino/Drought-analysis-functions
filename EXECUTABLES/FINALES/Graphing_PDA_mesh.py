# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 19:04:33 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import ColorMeshPDAGraphing

analysis = "NCDA"
variables = ['runoff', 'soil_moisture']
percentiles = [60, 65, 70, 75, 80, 85, 90, 95]

main_path = "E:/JC_FA_TESIS/"

dst_path = main_path + "Datos/Images/"

for variable in variables:
    for percentile in percentiles:
        db_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
    
        ColorMeshPDAGraphing(variable, 
                             percentile, 
                             db_path, 
                             analysis,
                             dst_path=dst_path)

