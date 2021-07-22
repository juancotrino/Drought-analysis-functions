# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 21:46:16 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import RastersToDataBase

variable = 'water_stress'

main_path = "E:/JC_FA_TESIS/"

start_date = "01-01-2000"
end_date = "31-12-2015"
src_filepath = main_path + "Datos/meteodata/total/water_stress/"
file_first_str = variable + "_"
file_second_str = ".tif" 
date_format = "%Y_%m_%d"
output_path = main_path + "Datos/DBs/model_results/" + variable + "/"

# src_filepath = main_path + "Datos/model_results/" + variable + "/"
# file_first_str = variable + "_"
# file_second_str = ".tif" 
# date_format = "%Y_%m_%d"
# output_path = main_path + "Datos/DBs/model_results/" + variable + "/"

RastersToDataBase(start_date,
                  end_date, 
                  variable,
                  src_filepath, 
                  file_first_str, 
                  file_second_str, 
                  date_format, 
                  output_path)