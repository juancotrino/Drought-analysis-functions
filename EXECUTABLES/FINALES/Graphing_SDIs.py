# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 17:00:00 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import SDIAnalysisGraphing

main_path = "E:/JC_FA_TESIS/"

row = 108
column = 88

sdi_name = ['SRI', 'SSI', 'SEDI']
sdi_intervals_analysis = [[1], [3], [6]]
dbs_path = [main_path + "Datos/DBs/SDI/SRI.pickle",
            main_path + "Datos/DBs/SDI/SSI.pickle",
            main_path + "Datos/DBs/SDI/SEDI.pickle"]

dst_path = main_path + "Datos/Images/"

for sdi_interval_analysis in sdi_intervals_analysis:
    SDIAnalysisGraphing(sdi_name,
                        sdi_interval_analysis,
                        dbs_path,
                        row, 
                        column,
                        dst_path=dst_path)


