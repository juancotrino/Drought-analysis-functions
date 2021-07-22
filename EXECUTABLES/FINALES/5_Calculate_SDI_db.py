# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 20:12:11 2020

@author: juan.cotrino
"""

from Hapi.droughtanalysis import MultipleSDICalculation
from Hapi.droughtanalysis import SDIClasses

main_path = "E:/JC_FA_TESIS/"

intervals = [1, 3, 6]

sdi_names = [
              'SRI',
              'SSI',
             'SEDI']

sdi_dbs_path = [
                main_path + "Datos/DBs/model_results/runoff/runoff_monthly_db.pickle",
                main_path + "Datos/DBs/model_results/soil_moisture/soil_moisture_monthly_db.pickle",
                main_path + "Datos/DBs/model_results/water_stress/water_stress_monthly_db.pickle"]

output_path = main_path + "Datos/DBs/SDI/"

MultipleSDICalculation(sdi_names, 
                        sdi_dbs_path, 
                        intervals, 
                        output_path)

SDIClasses(sdi_names, 
           sdi_dbs_path, 
           intervals, 
           output_path)


