import gdal
from datetime import datetime, timedelta

start = datetime.strptime("01-01-1979", "%d-%m-%Y")
end = datetime.strptime("31-12-2011", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

src_filepath = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/NETCDF/"
dst_filepath = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/prec/TIFF/"
shpfile_clip = '/Users/juanmanuel/Documents/OneDrive - ESCUELA COLOMBIANA DE INGENIERIA JULIO GARAVITO/1. TRABAJO DE GRADO/1. Tesis/2. Datos/0. Datos 20190912/Datos _iniciales/data/GIS/Mapa_General/cuenca_magdalena_proyectado.shp'

for date in date_generated:
    
    day = int(date.strftime("%Y%m%d"))
     
    d = datetime.strptime(str(day), '%Y%m%d')
    time_needed = [d + timedelta(hours = 12), d + timedelta(days = 1)]
    
    #Open existing dataset
    src_ds = gdal.Open( src_filepath + "CEMS_ECMWF_dis24_" + str(day) + "_glofas_v2.1.nc" )
    
    #Open output format driver, see gdal_translate --formats for list
    format = "GTiff"
    driver = gdal.GetDriverByName( format )
    
    #Output to new format
    dst_ds = dst_filepath + "daily-prec_" + str(day) + ".tif"
    
    #Reproject to different coordinate system
    gdal.Warp(dst_ds, 
              src_ds, 
              srcSRS='EPSG:4326', 
              dstSRS='EPSG:21897', 
              cutlineDSName=shpfile_clip,
              cropToCutline=True,
              dstNodata=0)
    
    #Properly close the datasets to flush to disk
    dst_ds = None
    src_ds = None