# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:42:27 2021

@author: juan.cotrino
"""

from Hapi.droughtanalysis import CDAAnalysis
from Hapi.droughtanalysis import ExportRastersFromCDADB

main_path = "E:/JC_FA_TESIS/"

percentiles = [60, 65, 70, 75, 80, 85, 90, 95]
variables = ['runoff', 'soil_moisture', 'water_stress']

for variable in variables:
    for percentile in percentiles:
        
        db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA/" + variable + "/drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
        output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/CDA/" + variable + "/"
        
        CDAAnalysis(variable, 
                    percentile, 
                    db_file, 
                    output_path)

        analyses = ['CDA']
        
        for analysis in analyses:
            reference_raster = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"
            output_path = main_path + "Datos/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable# + "/"
            if analysis == 'CDA':
                db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/" + "drought_clusters_" + variable + "_perc_" + str(percentile) + ".pickle" 
            
                ExportRastersFromCDADB(variable, 
                                       percentile, 
                                       db_file, 
                                       reference_raster, 
                                       output_path,
                                       pixel_type=5)


