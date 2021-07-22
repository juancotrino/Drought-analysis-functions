# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 00:46:08 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import PDASDIGraphing

sdis = ["SRI", "SSI", "SEDI"]
intervals = [1, 3, 6]

start_date = "01-06-2012"
end_date = "31-12-2013"

main_path = "E:/JC_FA_TESIS/"
dst_path = main_path + "Datos/Images/"

for sdi in sdis:

    db_path = main_path + "Datos/DBs/SDI/" + sdi + ".pickle"
        
    PDASDIGraphing(sdi, 
                   intervals, 
                   db_path,
                   separated=1,
                   dst_path=dst_path)