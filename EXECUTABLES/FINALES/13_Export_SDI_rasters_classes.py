# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 21:36:37 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import ExportRastersSDIClasses

sdis = ["SRI", "SSI", "SEDI"]
intervals = [1, 3, 6]

main_path = "E:/JC_FA_TESIS/"

reference_raster = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"

grl_output_path = main_path + "Datos/SDI"

for sdi in sdis:
    db_file = main_path + "Datos/DBs/SDI/" + sdi + "_classes.pickle"
    ExportRastersSDIClasses(sdi, 
                            intervals, 
                            db_file, 
                            reference_raster, 
                            grl_output_path)
    

     