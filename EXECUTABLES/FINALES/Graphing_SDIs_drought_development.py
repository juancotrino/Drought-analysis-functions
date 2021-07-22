# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 23:54:30 2021

@author: juan.cotrino
"""

from Hapi.datagraphing import RasterHorizontalGraphing

main_path = "E:/JC_FA_TESIS/"

reference_raster = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"

sdi_name = ['SRI', 'SSI', 'SEDI']
sdi_intervals_analysis = [1, 3, 6]
# sdi_name = ['SSI']
# sdi_intervals_analysis = [6]

dbs_path = [main_path + "Datos/DBs/SDI/SRI_classes.pickle",
            main_path + "Datos/DBs/SDI/SSI_classes.pickle",
            main_path + "Datos/DBs/SDI/SEDI_classes.pickle"]

# dbs_path = [main_path + "Datos/DBs/SDI/SSI_classes.pickle"]

date_range = ['01/09/2009', '01/10/2010']

dst_path = main_path + "Datos/Images/"

for sdi, db_path in zip(sdi_name, dbs_path):
    for interval in sdi_intervals_analysis:
        RasterHorizontalGraphing(main_path, 
                                 sdi, 
                                 interval,
                                 db_path, 
                                 date_range, 
                                 reference_raster,
                                 dst_path=dst_path)

