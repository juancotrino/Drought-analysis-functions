# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 00:12:37 2021

@author: juan.cotrino
"""

from Hapi.datagraphing import MonthlyDataGraphing

variable = 'runoff'

main_path = "E:/JC_FA_TESIS/"

start_date = "01-01-2000"
end_date = "31-12-2015"

dbs_path = main_path + "Datos/DBs/model_results/" + variable + "/" + variable + "_monthly_db.pickle"
dst_path = main_path + "Datos/Images/"

rows = [19, 47, 67, 103, 161, 170]
columns = [46, 67, 49, 57, 45, 41]

values = [0, 1, 2]

for value in values:
    for row, column in zip(rows, columns):
        MonthlyDataGraphing(variable,
                            dbs_path,
                            row,
                            column,
                            value=value,
                            dst_path=dst_path)