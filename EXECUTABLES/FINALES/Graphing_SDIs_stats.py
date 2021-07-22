# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 21:28:08 2021

@author: juan.cotrino
"""

from Hapi.datagraphing import RasterStatsGraphing

main_path = "E:/JC_FA_TESIS/"

sdi_names = ['SRI', 'SSI', 'SEDI']
intervals = [1, 3, 6]
reference_raster = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"

dst_path = main_path + "Datos/Images/"

stats = ['No_events',
          'Magnitude_mean',
          'Magnitude_standard_deviation', 
          'Magnitude_max',
          'Magnitude_min',
          'Duration_mean',
          'Duration_standard_deviation',
          'Duration_max']#,
          # 'Duration_min']

for stat in stats:
    RasterStatsGraphing(main_path, 
                        sdi_names, 
                        intervals, 
                        stat, 
                        reference_raster,
                        dst_path=dst_path)
    
