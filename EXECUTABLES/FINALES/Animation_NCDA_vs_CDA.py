# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 21:54:46 2020

@author: juan.cotrino
"""

from Hapi.datagraphing import NCDAVsCDAGraphing

# variable = 'runoff'
# percentile = 85

# variables = ["runoff", "soil_moisture", "water_stress"]
# percentiles = [60, 65, 70, 75, 80, 85, 90, 95]

# variables = ["runoff", "soil_moisture"]

variables = ["soil_moisture"]
percentiles = [80]

main_path = "E:/JC_FA_TESIS/"

start_date = "01-01-2009"
end_date = "31-12-2010"

# start_date = "20-06-2010"
# end_date = "23-06-2010"

analyses = ['NCDA',
            'CDA']

reference_raster = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"

dst_path = main_path + "Datos/Images/"

for variable in variables:
    for percentile in percentiles:

        db_files = [main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/NCDA/" + variable + "/" + "drought_binary_" + variable + "_perc_" + str(percentile) + ".pickle",
                    main_path + "Datos/DBs/NCDA_CDA/perc_" + str(percentile) + "/CDA/" + variable + "/" + "drought_clusters_" + variable + "_perc_" + str(percentile) + ".pickle"]
                    
        NCDAVsCDAGraphing(variable, 
                          percentile, 
                          analyses, 
                          db_files,
                          reference_raster,
                          start_date=start_date,
                          end_date=end_date,
                          dst_path=dst_path)


