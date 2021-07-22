# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 09:33:51 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import ComparisonPDANCDASDIGraphing


variables = ['runoff', 'soil_moisture']
# variables = ['runoff']#, 'soil_moisture']
percentiles = [60, 65, 70, 75, 80, 85, 90, 95]
# percentiles = [60]#, 65, 70, 75, 80, 85, 90, 95]
analysis = 'NCDA'

sdis = ['SRI', 'SSI']
# sdis = ['SRI']#, 'SSI']
intervals = [1, 3, 6]
# intervals = [1]#, 3, 6]

main_path = "E:/JC_FA_TESIS/"

dst_path = main_path + 'Datos/Images/'

for sdi, variable in zip(sdis, variables):
        
    sdi_db_path = main_path + "Datos/DBs/SDI/" + sdi + ".pickle"
    
    dbs_path = [main_path + "Datos/DBs/NCDA_CDA/perc_" + str(p) + "/" + analysis + "/" + variable + "/drought_binary_" + variable + "_perc_" + str(p) + ".pickle" for p in percentiles]

    ComparisonPDANCDASDIGraphing(variable,
                                 percentiles, 
                                 dbs_path, 
                                 analysis, 
                                 sdi, 
                                 intervals, 
                                 sdi_db_path,
                                 dst_path=dst_path)
        
