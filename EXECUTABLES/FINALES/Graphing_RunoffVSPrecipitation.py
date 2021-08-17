# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 23:18:55 2021

@author: juan.cotrino
"""

from Hapi.datagraphing import RunoffVSPrecipitationGraphing

main_path = "E:/JC_FA_TESIS/"

db_file_runoff = main_path + "Datos/DBs/model_results/runoff/runoff_monthly_db.pickle"
db_file_prec = main_path + "Datos/DBs/prec/prec_monthly_db.pickle"

cuencas_path = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/CUENCAS.tif"

# Alto Magdalena, Medio Magdalena, Bajo Magdalena (TOTAL), Cauca
rows = [132, 56, 1, 72]
columns = [50, 71, 48, 40]
cuencas_names = [1, 2, 3, 4]

dst_path = main_path + "Datos/Images/"

RunoffVSPrecipitationGraphing(db_file_runoff, 
                              db_file_prec, 
                              cuencas_path, 
                              rows, 
                              columns, 
                              cuencas_names, 
                              dst_path=dst_path)