# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 23:16:35 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import MultipleExportSDIStatsRasters

main_path = "E:/JC_FA_TESIS/"

sdi_names = [
             'SRI',
             'SSI',
             'SEDI']

sdi_dbs_path = [
                main_path + "Datos/DBs/model_results/runoff/runoff_monthly_db.pickle",
                main_path + "Datos/DBs/model_results/soil_moisture/soil_moisture_monthly_db.pickle",
                main_path + "Datos/DBs/model_results/water_stress/water_stress_monthly_db.pickle"]

intervals = [1, 3, 6]

db_files = [main_path + "Datos/DBs/SDI/" + sdi + ".pickle" for sdi in sdi_names]
reference_raster = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"
output_paths = [main_path + "Datos/SDI/" + sdi + "/stats/" for sdi in sdi_names]

MultipleExportSDIStatsRasters(sdi_names, 
                              intervals, 
                              db_files, 
                              reference_raster, 
                              output_paths)

