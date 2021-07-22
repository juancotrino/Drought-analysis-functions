# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 19:39:53 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import DroughtMultipleAreas

variables = ['soil_moisture']
analyses = ['CDA', 'NCDA']
percentiles = [85, 90]

main_path = "E:/JC_FA_TESIS/"

areas_path = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/RAS_DEP.tif"
codes_file = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/COD_DEP.xlsx"
area_column_name = 'DEPARTAMENTO'

for variable in variables:
    for analysis in analyses:
        for percentile in percentiles:

            db_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
            
            output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/"
            
            DroughtMultipleAreas(variable,
                                 percentile,
                                 areas_path, 
                                 db_path, 
                                 area_column_name,
                                 codes_file, 
                                 output_path)

