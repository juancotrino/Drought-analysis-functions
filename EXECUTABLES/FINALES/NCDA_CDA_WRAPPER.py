# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 14:57:02 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import MonthlyPercentile
from Hapi.droughtanalysis import GetThresholdSeries
from Hapi.droughtanalysis import BinaryDroughtPercentile
from Hapi.droughtanalysis import NCDACleaning
from Hapi.droughtanalysis import CDAAnalysis
from Hapi.droughtanalysis import ExportRastersFromDB
from Hapi.droughtanalysis import ExportRastersFromCDADB

# variables = ['runoff', 'soil_moisture', 'water_stress']
# percentiles = [60, 65, 70, 75, 80, 85, 90, 95]

variables = ['water_stress']
percentiles = [60, 65, 70, 75, 80, 85, 90, 95]

main_path = "E:/JC_FA_TESIS/"

for variable in variables:
    for percentile in percentiles:

        db_file = main_path + "Datos/DBs/model_results/" + variable + "/" + variable + "_daily_db.pickle"
        output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/thresholds/" + variable + "/"
        
        MonthlyPercentile(db_file, 
                          percentile, 
                          variable, 
                          output_path)
        
        
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
        
        db_file = main_path + "Datos/DBs/model_results/" + variable + "/" + variable + "_daily_db.pickle"
        src_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/thresholds/" + variable + "/"
        smoothed_threshold = [src_path + "smoothed_threshold_monthly_perc_" + str(percentile) + "_leap_year.pickle",
                              src_path + "smoothed_threshold_monthly_perc_" + str(percentile) + "_regular_year.pickle"]
        output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA_raw/" + variable + "/"
        
        BinaryDroughtPercentile(variable, 
                                percentile, 
                                db_file, 
                                smoothed_threshold, 
                                output_path)
        
        db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA_raw/" + variable + "/" + "drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
        output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA/" + variable + "/"
        
        NCDACleaning(variable, 
                     percentile, 
                     db_file, 
                     output_path)
        
        db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA/" + variable + "/drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"
        output_path = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/CDA/" + variable + "/"
        
        CDAAnalysis(variable, 
                    percentile, 
                    db_file, 
                    output_path)
        
        analyses = ['NCDA_raw', 'NCDA', 'CDA']
        
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

            else:
                db_file = main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/" + analysis + "/" + variable + "/" + "drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle" 
            
                ExportRastersFromDB(variable, 
                                    percentile, 
                                    db_file, 
                                    reference_raster, 
                                    output_path,
                                    pixel_type=5)

