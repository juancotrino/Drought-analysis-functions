# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:08:25 2021

@author: juan.cotrino
"""

from Hapi.datagraphing import NumberOfClustersGraphing

main_path = "E:/JC_FA_TESIS/"

variables = ['runoff', 'soil_moisture', 'water_stress']
percentiles = [60, 65, 70, 75, 80, 85, 90, 95]
dst_path = main_path + "Datos/Images/"

for variable in variables:
    for percentile in percentiles:

        db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/CDA/" + variable + "/drought_clusters_" + variable + "_perc_" + str(percentile) + ".pickle"
        
        NumberOfClustersGraphing(variable, 
                                 percentile, 
                                 db_file,
                                 dst_path=dst_path)
