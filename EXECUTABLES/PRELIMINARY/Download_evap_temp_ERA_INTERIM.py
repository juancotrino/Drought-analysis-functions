#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:08:09 2020

@author: juanmanuel
"""

import watools as wa
import shutil
import os

Dir = '/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/'
Var = ['T','E']
Startdate = '2000-01-01'
Enddate = '2005-12-31'
latlim = [1.57, 11.1]
lonlim = [-76.93, -72.2]

wa.Collect.ECMWF.daily(Dir,
                       Var,
                       Startdate,
                       Enddate,
                       latlim,
                       lonlim)

shutil.move("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/Weather_Data/Model/ECMWF/daily/Evaporation/mean",
            "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/evap/")
os.rename("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/evap/mean",
          "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/evap/ERA_INTERIM")

shutil.move("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/Weather_Data/Model/ECMWF/daily/Tair2m/mean",
            "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/temp/")
os.rename("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/temp/mean",
          "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/temp/ERA_INTERIM")

shutil.rmtree("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/Weather_Data")