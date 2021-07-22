#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:08:09 2020

@author: juanmanuel
"""

import watools as wa
import shutil
import os

Dir = '/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/prec/'
Startdate = '1991-03-21'
Enddate = '2011-12-31'
latlim = [1.57, 11.1]
lonlim = [-76.93, -72.2]

wa.Collect.CHIRPS.daily(Dir, 
                        Startdate,
                        Enddate,
                        latlim, 
                        lonlim)

shutil.move("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/prec/Precipitation/CHIRPS/Daily",
            "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/prec/")
os.rename("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/prec/Daily",
          "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/prec/CHIRPS")
shutil.rmtree("/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/prec/Precipitation")