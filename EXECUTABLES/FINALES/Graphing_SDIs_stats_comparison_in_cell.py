# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 22:23:39 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import DroughtEventsNumberSDIGraphing

main_path = "E:/JC_FA_TESIS/"

sdi_names = ['SRI', 'SSI', 'SEDI']
intervals = [1, 3, 6]
db_files = [main_path + "Datos/DBs/SDI/SRI.pickle",
            main_path + "Datos/DBs/SDI/SSI.pickle",
            main_path + "Datos/DBs/SDI/SEDI.pickle"]

row = 19
column = 46

dst_path = main_path + "Datos/Images/"

DroughtEventsNumberSDIGraphing(sdi_names,
                               intervals,
                               db_files, 
                               row, 
                               column,
                               dst_path=dst_path)