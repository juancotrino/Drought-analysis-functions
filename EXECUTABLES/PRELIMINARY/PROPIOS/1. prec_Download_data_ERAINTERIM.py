# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from ecmwfapi import ECMWFDataServer
from datetime import datetime, timedelta
 
start = datetime.strptime("01-01-1979", "%d-%m-%Y")
end = datetime.strptime("29-03-1979", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

for date in date_generated:
    server = ECMWFDataServer()
    server.retrieve({
        "class"  : "ei",
        "dataset": "interim",
        "date"   : str(date),
        "expver" : "1",
        "grid"   : "0.05/0.05",
        "area"   : "11.1/-76.93/1.57/-72.2",
        "levtype": "sfc",
        "param"  : "228.128",
        "step"   : "12",
        "stream" : "oper",
        "time"   : "00:00:00/12:00:00",
        "type"   : "fc",
        "format" : "netcdf",
        "target" : "NETCDF_files/MID/prec_" + str(date.strftime("%Y%m%d")) + ".nc",
    })