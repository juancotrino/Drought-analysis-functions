# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 01:18:22 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import PDAGraphing

variables = ["runoff", "soil_moisture", "water_stress"]
percentiles = [60, 65, 70, 75, 80, 85, 90, 95]
analysis_names = ['NCDA']

start_date = "01-06-2012"
end_date = "31-12-2013"

main_path = "E:/JC_FA_TESIS/"

for variable in variables:

    dbs_path = [main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/CDA/" + variable + "/drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle" for percentile in percentiles]
    
    dst_path = main_path + "Datos/Images/"
    
    PDAGraphing(variable,
                percentiles,
                dbs_path,
                analysis_names,
                # start_date=start_date,
                # end_date=end_date,
                separated=1,
                dst_path=dst_path)
            
import requests
