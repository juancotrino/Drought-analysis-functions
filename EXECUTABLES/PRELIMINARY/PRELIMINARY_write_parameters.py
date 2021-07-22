#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 20:14:02 2020

@author: juanmanuel
"""

import Hapi.distparameters as DP
from osgeo import gdal

main_path = "C:/Users/juan.cotrino/Documents/JC_FA_TESIS/"
FlowAccPath = main_path + "Datos/GIS/Mapa_General/RASTERS_CUENCA/flow_acc.tif"
SpatialVarFun = DP.par3dLumped
raster = gdal.Open(FlowAccPath)
no_parameters = 12
lumpedParNo = 0
lumped_par_pos = []
snow = 0
kub = 3
klb = 0.5
Path = main_path + "Datos/Calibration/Parameters/"

par = [7.52485353e-01,  #rfcf
       3.73465581e+02,  #FC
       1.93999492e+00,  #BETA
       2.26894609e-01,  #ETF
       2.61787427e-01,  #LP
       4.84998412e-04,  #CFLUX
       1.0e-02,  #K
       3.92952291e-02,  #K1
       1.05974027e-02,  #ALPHA
       4.37981548e+00,  #PERC
       9.60547407e+01,  #kposition
       8.48260859e-03]  #xmuskingum

DP.SaveParameters(SpatialVarFun, 
                  raster, 
                  par, 
                  no_parameters,
                  lumpedParNo, 
                  lumped_par_pos,
                  snow,
                  kub,
                  klb,
                  Path)

print('\a')

