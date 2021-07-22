# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 22:42:58 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import ModelResultsGraphing

variable = 'runoff'
variable_unit = "m3/s"

main_path = "E:/JC_FA_TESIS/"

start_date = "01-01-2011"
end_date = "31-12-2013"
valid_start_date = "01-01-2012"
db_observed = main_path + "Datos/Calibration/Discharge/Qobs_IDEAM.xlsx"
obs_sheet = 'Sheet1'
coor_sheet = 'coordinates'
db_simulated = main_path + "Datos/DBs/model_results/" + variable + "/" + variable + "_daily_db.pickle"
ref_raster = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"

rows = [19, 47, 67, 103, 161, 170]
columns = [46, 67, 49, 57, 45, 41]

dst_path = main_path + "Datos/Images/"

for row, column in zip(rows, columns):

    ModelResultsGraphing(variable, 
                         variable_unit, 
                         db_observed, 
                         obs_sheet, 
                         coor_sheet, 
                         db_simulated, 
                         row, 
                         column, 
                         ref_raster,
                         # start_date=start_date,
                         # end_date=end_date,
                         dst_path=dst_path,
                         valid_start_date=valid_start_date)




