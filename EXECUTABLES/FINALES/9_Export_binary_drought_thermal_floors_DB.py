# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 19:39:53 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import DroughtMultipleElevations

variables = ['runoff', 'soil_moisture']
analyses = ['CDA', 'NCDA']
percentiles = [85, 90]


dict_elev = {'Cálido'               : [-100, 1000],
             'Templado'             : [1000, 2000],
             'Frío'                 : [2000, 3000],
             'Muy frío'             : [3000, 3600],
             'Extremadamente frío'  : [3600, 4200],
             'Subnival'             : [4200, 4700],
             'Nival'                : [4700, 5775]}

main_path = "E:/JC_FA_TESIS/"

dem_path = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"

for variable in variables:
    for analysis in analyses:
        for percentile in percentiles:

            db_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
            
            output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/"
            
            DroughtMultipleElevations(variable,
                                      percentile,
                                      dem_path, 
                                      db_path, 
                                      dict_elev, 
                                      output_path)

