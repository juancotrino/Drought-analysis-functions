# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:00:54 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import ColorMeshPDASDIGraphing

sdis = ["SRI", "SSI", "SEDI"]
intervals = [1, 3, 6]

main_path = "E:/JC_FA_TESIS/"

dst_path = main_path + "Datos/Images/"

for sdi in sdis:
    db_path = main_path + "Datos/DBs/SDI/" + sdi + ".pickle"

    ColorMeshPDASDIGraphing(sdi, 
                            intervals, 
                            db_path,
                            dst_path=dst_path)

