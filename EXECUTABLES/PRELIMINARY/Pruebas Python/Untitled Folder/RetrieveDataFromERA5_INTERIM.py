# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:10:59 2019

@author: jmcotrino
"""
#The code below, downloads different parameters and store the netCDF file identifying the parameter for each file.

from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer()

#Parameters
parameter_name_list = ["evaporation",
                       "temperature"]

parameter_code_list = ["182",
                       "167"]

#Dates in format YYYY-MM-DD, the initial date of the dataset from INTERIM is the 1st of January 1979
date_from   = "1979-01-01"
date_to     = "1979-06-01"
#date_to     = "2011-10-10"

#Cell size
lat = "0.05"
lon = "0.05"

#Retrieve
for parameter_name, parameter_code in zip(parameter_name_list, parameter_code_list):

    server.retrieve({
        "class": "ei",
        "dataset": "interim",
        "expver": "1",
        "stream": "oper",
        "type": "fc",
        "levtype": "sfc",
        "param": parameter_code + ".128", 
        "date": date_from + "/to/" + date_to,
        "time": "00:00:00",
        "step": "24",
        "grid": lat + "/" + lon,
        "area":"11.1/-76.93/1.57/-72.2",
        "format":"netcdf",
        "target": "Downloads_ERAINTERIM/" + parameter_name + "/" + date_from + "_to_" + date_to + "_" + parameter_name + ".nc"
    })

#Retreive precipitation data in a separate way
server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "expver": "1",
    "stream": "oper",
    "type": "fc",
    "levtype": "sfc",
    "param": "228.128", 
    "date": date_from + "/to/" + date_to,
    "time": "00:00:00/12:00:00",
    "step": "12",
    "grid": lat + "/" + lon,
    "area":"11.1/-76.93/1.57/-72.2",
    "format":"netcdf",
    "target": "Downloads_ERAINTERIM/precipitation/" + date_from + "_to_" + date_to + "_precipitation.nc"
})