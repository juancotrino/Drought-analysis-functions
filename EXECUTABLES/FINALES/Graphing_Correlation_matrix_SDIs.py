# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 15:44:13 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import CorrMatrixGraphing

main_path = "E:/JC_FA_TESIS/"

sdi_names = ['SRI', 'SSI', 'SEDI']
intervals = [1, 3, 6]
db_files = [main_path + "Datos/DBs/SDI/SRI.pickle",
            main_path + "Datos/DBs/SDI/SSI.pickle",
            main_path + "Datos/DBs/SDI/SEDI.pickle"]

dst_path = main_path + "Datos/Images/"

CorrMatrixGraphing(sdi_names, 
                   intervals, 
                   db_files, 
                   dst_path=dst_path)

