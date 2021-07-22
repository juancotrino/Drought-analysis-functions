# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 14:41:14 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import ExportRastersFromDB

# variables = ['runoff', 'soil_moisture', 'water_stress']
analysis = 'NCDA'
# percentiles = [60, 65, 70, 75, 80, 90, 95]

variables = ['runoff']
percentiles = [60]

main_path = "E:/JC_FA_TESIS/"

for percentile in percentiles:
    for variable in variables:

        db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/" + "drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle" 
        reference_raster = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"
        output_path = main_path + "Datos/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/"
        
        ExportRastersFromDB(variable, 
                            percentile, 
                            db_file, 
                            reference_raster, 
                            output_path, 
                            pixel_type=5)
