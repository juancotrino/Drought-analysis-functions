# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:24:42 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import PDAThermalFloorsGraphing

variable = "soil_moisture"
percentile = 90
analysis_names = ['NCDA']#,
                  # 'CDA']

start_date = "01-01-2000"
end_date = "31-12-2015"

main_path = "E:/JC_FA_TESIS/"

dbs_path = [main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA/" + variable + "/drought_binary_thermal_floors_" + variable + "_perc_" + str(percentile) + ".pickle"]#,
            # main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/CDA/" + variable + "/drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle"]
identifier = "thermal_floors"

# dbs_path = [main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA/" + variable + "/drought_binary_areas_" + variable + "_perc_" + str(percentile) + ".pickle"]#,
#             # main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/CDA/" + variable + "/drought_binary_areas_" + variable + "_perc_" + str(percentile) + ".pickle"]
# identifier = "departments"

dst_path = main_path + "Datos/Images/"

PDAThermalFloorsGraphing(variable, 
                         percentile, 
                         dbs_path, 
                         identifier,
                         analysis_names,
                         respect_to=0,
                         separated=1,
                         dst_path=dst_path)

