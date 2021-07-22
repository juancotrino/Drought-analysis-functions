#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 18:13:16 2020

@author: juanmanuel
"""

from datetime import datetime, timedelta
# from Hapi import raster as GIS
from osgeo import gdal, gdalconst

dem_path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/GIS/Mapa_General/RASTERS_CUENCA/DEM.tif"
input_raster_path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata_RAW/calib/"
output_raster_path = "/Users/juanmanuel/Documents/Juan Manuel/Universidad/TESIS/Datos/meteodata/calib/"

start = datetime.strptime("01-01-1981", "%d-%m-%Y")
end = datetime.strptime("02-01-1981", "%d-%m-%Y")
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]

import numpy as np
import ogr
import osr
from pyproj import Proj, transform


#------------------------------

def MatchRasterAlignment(RasterA,RasterB):
    """
    =========================================================================
      MatchRasterAlignment(RasterA,RasterB)
    =========================================================================
    this function matches the coordinate system and the number of of rows & columns
    between two rasters
    Raster A is the source of the coordinate system, no of rows and no of columns & cell size
    Raster B is the source of data values in cells
    the result will be a raster with the same structure like RasterA but with
    values from RasterB using Nearest Neighbour interpolation algorithm

    Inputs:
    ----------
        1- RasterA:
            [gdal.dataset] spatial information source raster to get the spatial information
            (coordinate system, no of rows & columns)
        2- RasterB:
            [gdal.dataset] data values source raster to get the data (values of each cell)

    Outputs:
    ----------
        1- dst:
            [gdal.dataset] result raster in memory

    Example:
    ----------
        A=gdal.Open("dem4km.tif")
        B=gdal.Open("P_CHIRPS.v2.0_mm-day-1_daily_2009.01.06.tif")
        matched_raster=MatchRasters(A,B)
    """
    # input data validation
    # data type
    assert type(RasterA)==gdal.Dataset, "RasterA should be read using gdal (gdal dataset please read it using gdal library) "
    assert type(RasterB)==gdal.Dataset, "RasterB should be read using gdal (gdal dataset please read it using gdal library) "

    gt_src=RasterA
    # we need number of rows and cols from src A and data from src B to store both in dst
    gt_src_proj=gt_src.GetProjection()
    # GET THE GEOTRANSFORM
    gt_src_gt=gt_src.GetGeoTransform()
    # GET NUMBER OF columns
    gt_src_x=gt_src.RasterXSize
    # get number of rows
    gt_src_y=gt_src.RasterYSize

    gt_src_epsg=osr.SpatialReference(wkt=gt_src_proj)
#    gt_src_epsg.GetAttrValue('AUTHORITY',1)

    # unite the crs
    # TODO still doesn't work with all projections better to use UTM zones for the moment
    data_src=ProjectRaster(RasterB,int(gt_src_epsg.GetAttrValue('AUTHORITY',1)))
        
    
    
    # create a new raster
    mem_drv=gdal.GetDriverByName("MEM")
    dst=mem_drv.Create("",gt_src_x,gt_src_y,1,gdalconst.GDT_Float32) #,['COMPRESS=LZW'] LZW is a lossless compression method achieve the highst compression but with lot of computation
    # set the geotransform
    dst.SetGeoTransform(gt_src_gt)
    # set the projection
    dst.SetProjection(gt_src_epsg.ExportToWkt())
    # set the no data value
    dst.GetRasterBand(1).SetNoDataValue(gt_src.GetRasterBand(1).GetNoDataValue())
    # initialize the band with the nodata value instead of 0
    dst.GetRasterBand(1).Fill(gt_src.GetRasterBand(1).GetNoDataValue())
    # perform the projection & resampling
    resample_technique=gdal.GRA_NearestNeighbour #gdal.GRA_NearestNeighbour

    gdal.ReprojectImage(data_src,dst,gt_src_epsg.ExportToWkt(),gt_src_epsg.ExportToWkt(),resample_technique)

#    SaveRaster(dst,"colombia/newraster.tif")
    return dst


def ProjectRaster(src, to_epsg,resample_technique="Nearest"): #raster.py FUNCTION
    """
    =====================================================================
        project_dataset(src, to_epsg):
    =====================================================================
    this function reproject a raster to any projection
    (default the WGS84 web mercator projection, without resampling)
    The function returns a GDAL in-memory file object, where you can ReadAsArray etc.

    inputs:
    ----------
        1- raster:
            gdal dataset (src=gdal.Open("dem.tif"))
        2-to_epsg:
            integer reference number to the new projection (https://epsg.io/)
            (default 3857 the reference no of WGS84 web mercator )
        3-cell_size:
            integer number to resample the raster cell size to a new cell size
            (default empty so raster will not be resampled)
        4- resample_technique:
            [String] resampling technique default is "Nearest"
            https://gisgeography.com/raster-resampling/
            "Nearest" for nearest neighbour,"cubic" for cubic convolution,
            "bilinear" for bilinear

    Outputs:
    ----------
        1-raster:
            gdal dataset (you can read it by ReadAsArray)

    Ex:
    ----------
        projected_raster=project_dataset(src, to_epsg=3857)
    """
    #### input data validation
    # data type
    assert type(src)==gdal.Dataset, "src should be read using gdal (gdal dataset please read it using gdal library) "
    assert type(to_epsg)==int,"please enter correct integer number for to_epsg more information https://epsg.io/"
    assert type(resample_technique)== str ," please enter correct resample_technique more information see docmentation "

    if resample_technique=="Nearest":
        resample_technique=gdal.GRA_NearestNeighbour
    elif resample_technique=="cubic":
        resample_technique=gdal.GRA_Cubic
    elif resample_technique=="bilinear":
        resample_technique=gdal.GRA_Bilinear

    ### Source raster
    # GET PROJECTION
    src_proj=src.GetProjection()
    # GET THE GEOTRANSFORM
    src_gt=src.GetGeoTransform()
    # GET NUMBER OF columns
    src_x=src.RasterXSize
    # get number of rows
    src_y=src.RasterYSize
    # number of bands
#    src_bands=src.RasterCount
    # spatial ref
    src_epsg=osr.SpatialReference(wkt=src_proj)
    
    print('El valor máximo del raster leido es: {0}, y el valor mínimo es: {1}'.format(np.max(src.ReadAsArray()), np.min(src.ReadAsArray())))

    
    ### distination raster
    # spatial ref
    dst_epsg=osr.SpatialReference()
    dst_epsg.ImportFromEPSG(to_epsg)
    # transformation factors
    tx = osr.CoordinateTransformation(src_epsg,dst_epsg)

    # in case the source crs is GCS and longitude is in the west hemisphere gdal
    # reads longitude fron 0 to 360 and transformation factor wont work with valeus
    # greater than 180
    print('Antes del primer if')
    if src_epsg.GetAttrValue('AUTHORITY',1) != str(to_epsg) :
        print('Antes del segundo if')
        if src_epsg.GetAttrValue('AUTHORITY',1)=="4326" and src_gt[0] > 180:
            
            lng_new=src_gt[0]-360
            # transform the right upper corner point
            (ulx,uly,ulz) = tx.TransformPoint(lng_new, src_gt[3])
            # transform the right lower corner point
            (lrx,lry,lrz)=tx.TransformPoint(lng_new+src_gt[1]*src_x,
                                            src_gt[3]+src_gt[5]*src_y)
        else:
            print("Entró")
            # transform the right upper corner point
            (ulx,uly,ulz) = tx.TransformPoint(src_gt[0], src_gt[3])
            # transform the right lower corner point
            (lrx,lry,lrz)=tx.TransformPoint(src_gt[0]+src_gt[1]*src_x,
                                            src_gt[3]+src_gt[5]*src_y)
            print(ulx, uly,ulz,lrx,lry,lrz)
    else:
        ulx = src_gt[0]
        uly = src_gt[3]
#        ulz = 0
        lrx = src_gt[0]+src_gt[1]*src_x
        lry = src_gt[3]+src_gt[5]*src_y
#        lrz = 0


    # get the cell size in the source raster and convert it to the new crs
    # x coordinates or longitudes
    xs=[src_gt[0],src_gt[0]+src_gt[1]]
    # y coordinates or latitudes
    ys=[src_gt[3],src_gt[3]]
    
    print(xs,ys)
    
    print("Antes del if")
    
    if src_epsg.GetAttrValue('AUTHORITY',1) != str(to_epsg):
        print(ys,xs,int(src_epsg.GetAttrValue('AUTHORITY',1)),int(dst_epsg.GetAttrValue('AUTHORITY',1)))
        # transform the two points coordinates to the new crs to calculate the new cell size
        new_xs, new_ys= ReprojectPoints(ys,xs,from_epsg=int(src_epsg.GetAttrValue('AUTHORITY',1)),
                                          to_epsg=int(dst_epsg.GetAttrValue('AUTHORITY',1)))
        print(new_xs,new_ys)
    else:
        new_xs = xs
        new_ys = ys

    pixel_spacing=np.abs(new_xs[0]-new_xs[1])
    
# #(*****************************************THIS IS THE CODE FROM GISpy.py********************************************)
#     # create a new raster 
#     mem_drv=gdal.GetDriverByName("MEM")
#     dst=mem_drv.Create("",int(np.round((lrx-ulx)/pixel_spacing)),int(np.round((uly-lry)/pixel_spacing)),
#                         1,gdalconst.GDT_Float32) #['COMPRESS=LZW'] LZW is a lossless compression method achieve the highst compression but with lot of computation

# #(*******************************************************************************************************************)

    # create a new raster
    mem_drv=gdal.GetDriverByName("MEM")
    dst=mem_drv.Create("",int(np.round((lrx-ulx)/pixel_spacing)),int(np.round((lry-uly)/pixel_spacing)),
                        1,gdalconst.GDT_Float32) #['COMPRESS=LZW'] LZW is a lossless compression method achieve the highst compression but with lot of computation

    # new geotransform
    new_geo=(ulx,pixel_spacing,src_gt[2],uly,src_gt[4],-pixel_spacing)
    
    print('El valor máximo del raster leido y reproyectado después de creadoes: {0}, y el valor mínimo es: {1}'.format(np.max(dst.ReadAsArray()), np.min(dst.ReadAsArray())))
    
    # set the geotransform
    dst.SetGeoTransform(new_geo)
    # set the projection
    dst.SetProjection(dst_epsg.ExportToWkt())
    # set the no data value
    dst.GetRasterBand(1).SetNoDataValue(src.GetRasterBand(1).GetNoDataValue())
    # initialize the band with the nodata value instead of 0
    dst.GetRasterBand(1).Fill(src.GetRasterBand(1).GetNoDataValue())
    # perform the projection & resampling
    gdal.ReprojectImage(src,dst,src_epsg.ExportToWkt(),dst_epsg.ExportToWkt(),resample_technique)

    print('El valor máximo del raster leido y reproyectado es: {0}, y el valor mínimo es: {1}'.format(np.max(dst.ReadAsArray()), np.min(dst.ReadAsArray())))



    return dst




def ReprojectPoints(lat,lng,from_epsg=4326,to_epsg=3857):
    """
    =====================================================================
      reproject_points(lat, lng, from_epsg=4326,to_epsg=3857)
    =====================================================================
    this function change the projection of the coordinates from a coordinate system
    to another (default from GCS to web mercator used by google maps)

    Inputs:
    ----------
        1- lat:
            list of latitudes of the points
        2- lng:
            list of longitude of the points
        3- from_epsg:
            integer reference number to the projection of the points (https://epsg.io/)
        4- to_epsg:
            integer reference number to the new projection of the points (https://epsg.io/)

    outputs:
    ----------
        1-x:
            list of x coordinates of the points
        2-y:
            list of y coordinates of the points

    Ex:
    ----------
        # from web mercator to GCS WGS64:
        x=[-8418583.96378159, -8404716.499972705], y=[529374.3212213353, 529374.3212213353]
        from_epsg = 3857, to_epsg = 4326
        longs, lats=reproject_points(y,x,from_epsg="3857", to_epsg="4326")
    """
    from_epsg="epsg:"+str(from_epsg)
    inproj = Proj(init=from_epsg) # GCS geographic coordinate system
    to_epsg="epsg:"+str(to_epsg)
    outproj=Proj(init=to_epsg) # WGS84 web mercator

    x=np.ones(len(lat))*np.nan
    y=np.ones(len(lat))*np.nan

    for i in range(len(lat)):
        x[i],y[i]=transform(inproj,outproj,lng[i],lat[i])

    return x,y


def MatchNoDataValue(src,dst):
    """
    ==================================================================
      MatchNoDataValue(src,dst)
    ==================================================================
    this function matches the location of nodata value from src raster to dst
    raster, Both rasters have to have the same dimensions (no of rows & columns)
    so MatchRasterAlignment should be used prior to this function to align both
    rasters


    inputs:
    ----------
        1-src:
            [gdal.dataset] source raster to get the location of the NoDataValue and
            where it is in the array
        1-dst:
            [gdal.dataset] raster you want to store NoDataValue in its cells
            exactly the same like src raster

    Outputs:
    ----------
        1- dst:
            [gdal.dataset] the second raster with NoDataValue stored in its cells
            exactly the same like src raster
    """
    # input data validation
    # data type
    assert type(src)==gdal.Dataset, "src should be read using gdal (gdal dataset please read it using gdal library) "
    assert type(dst)==gdal.Dataset, "dst should be read using gdal (gdal dataset please read it using gdal library) "

    src_gt=src.GetGeoTransform()
    src_proj=src.GetProjection()
    src_row=src.RasterYSize
    src_col=src.RasterXSize
    src_noval=np.float32(src.GetRasterBand(1).GetNoDataValue())
    src_sref=osr.SpatialReference(wkt=src_proj)
    src_epsg=int(src_sref.GetAttrValue('AUTHORITY',1))

    src_array=src.ReadAsArray()
    print('El valor máximo del array origen: {0}, y el valor mínimo es: {1}'.format(np.max(src_array), np.min(src_array)))
    dst_gt=dst.GetGeoTransform()
    dst_proj=dst.GetProjection()
    dst_row=dst.RasterYSize
    dst_col=dst.RasterXSize

    dst_sref=osr.SpatialReference(wkt=dst_proj)
    dst_epsg=int(dst_sref.GetAttrValue('AUTHORITY',1))
    
    print('El EPSG de origen es: {0}, y el de destino es {1}'.format(src_epsg,dst_epsg))

    #check proj
    assert src_row==dst_row and src_col==dst_col, "two rasters has different no of columns or rows please resample or match both rasters"
    assert dst_gt==src_gt, "location of upper left corner of both rasters are not the same or cell size is different please match both rasters first "
    assert src_epsg == dst_epsg, "Raster A & B are using different coordinate system please reproject one of them to the other raster coordinate system"
    

# #(*****************************************THIS IS THE CODE FROM GISpy.py********************************************)

    # dst_array = dst.ReadAsArray()

# #(*******************************************************************************************************************)

    dst_array = np.float32(dst.ReadAsArray())
    print('El valor máximo del array destino: {0}, y el valor mínimo es: {1}'.format(np.max(dst_array), np.min(dst_array)))
    dst_array[src_array==src_noval] = src_noval

    # align function only equate the no of rows and columns only
    # match nodatavalue inserts nodatavalue in dst raster to all places like src
    # still places that has nodatavalue in the dst raster but it is not nodatavalue in the src
    # and now has to be filled with values
    # compare no of element that is not nodata value in both rasters to make sure they are matched
    elem_src = np.size(src_array[:,:])-np.count_nonzero((src_array[src_array==src_noval]))
    elem_dst = np.size(dst_array[:,:])-np.count_nonzero((dst_array[dst_array==src_noval]))
    # if not equal then store indices of those cells that doesn't matchs
    if elem_src > elem_dst :
        rows=[i for i in range(src_row) for j in range(src_col) if dst_array[i,j]==src_noval and src_array[i,j] != src_noval]
        cols=[j for i in range(src_row) for j in range(src_col) if dst_array[i,j]==src_noval and src_array[i,j] != src_noval]
    # interpolate those missing cells by nearest neighbour
    
    print(np.max(dst_array), src_noval, len(rows), len(cols))
    print(dst_array.shape)
    
    if elem_src > elem_dst :
        dst_array = NearestNeighbour(dst_array, src_noval, rows, cols)

    

    mem_drv=gdal.GetDriverByName("MEM")
    dst=mem_drv.Create("",src_col,src_row,1,gdalconst.GDT_Float32) #,['COMPRESS=LZW'] LZW is a lossless compression method achieve the highst compression but with lot of computation
    
    # set the geotransform
    dst.SetGeoTransform(src_gt)
    # set the projection
    dst.SetProjection(src_sref.ExportToWkt())
    # set the no data value
    dst.GetRasterBand(1).SetNoDataValue(src.GetRasterBand(1).GetNoDataValue())
    # initialize the band with the nodata value instead of 0
    dst.GetRasterBand(1).Fill(src.GetRasterBand(1).GetNoDataValue())
    dst.GetRasterBand(1).WriteArray(dst_array)

    return dst

def NearestNeighbour(array, Noval, rows, cols): #ESTA FUNCIÓN ES IGUAL EN raster.py Y GISpy.py
    """
    ===============================================================
        NearestNeighbour(array, Noval, rows, cols)
    ===============================================================
    this function filles cells of a given indices in rows and cols with
    the value of the nearest neighbour.
    as the raster grid is square so the 4 perpendicular direction are of the same
    close so the function give priority to the right then left then bottom then top
    and the same for 45 degree inclined direction right bottom then left bottom
    then left Top then right Top

    Inputs:
    ----------
        1-array:
            [numpy.array] Array to fill some of its cells with Nearest value.
        2-Noval:
            [float32] value stored in cells that is out of the domain
        3-rows:
            [List] list of the row index of the cells you want to fill it with
            nearest neighbour.
        4-cols:
            [List] list of the column index of the cells you want to fill it with
            nearest neighbour.

    Output:
    ----------
        - array:
            [numpy array] Cells of given indices will be filled with value of the Nearest neighbour

    Example:
    ----------
        - raster=gdal.opne("dem.tif")
          rows=[3,12]
          cols=[9,2]
          new_array=NearestNeighbour(rasters, rows, cols)
    """
    #### input data validation
    # data type
    assert type(array)==np.ndarray , "src should be read using gdal (gdal dataset please read it using gdal library) "
    assert type(rows) == list,"rows input has to be of type list"
    assert type(cols) == list,"cols input has to be of type list"


#    array=raster.ReadAsArray()
    # Noval=np.float32(raster.GetRasterBand(1).GetNoDataValue())
#    no_rows=raster.RasterYSize
    no_rows=np.shape(array)[0]
#    no_cols=raster.RasterXSize
    no_cols=np.shape(array)[1]
    
    print(no_rows,no_cols,Noval,len(rows),len(cols), np.max(array))
    
    
    for i in range(len(rows)):
        # give the cell the value of the cell that is at the right
        if array[rows[i],cols[i]+1] != Noval and cols[i]+1 <= no_cols:
            array[rows[i],cols[i]] = array[rows[i],cols[i]+1]

        elif array[rows[i],cols[i]-1] != Noval and cols[i]-1 > 0 :
            # give the cell the value of the cell that is at the left
            array[rows[i],cols[i]] = array[rows[i],cols[i]-1]

        elif array[rows[i]-1,cols[i]] != Noval and rows[i]-1 > 0:
        # give the cell the value of the cell that is at the bottom
            array[rows[i],cols[i]] = array[rows[i]-1,cols[i]]

        elif array[rows[i]+1,cols[i]] != Noval and rows[i]+1 <= no_rows:
        # give the cell the value of the cell that is at the Top
            array[rows[i],cols[i]] = array[rows[i]+1,cols[i]]

        elif array[rows[i]-1,cols[i]+1] != Noval and rows[i]-1 > 0 and cols[i]+1 <=no_cols :
        # give the cell the value of the cell that is at the right bottom
            array[rows[i],cols[i]] = array[rows[i]-1,cols[i]+1]

        elif array[rows[i]-1,cols[i]-1] != Noval and rows[i]-1 >0 and cols[i]-1 > 0:
        # give the cell the value of the cell that is at the left bottom
            array[rows[i],cols[i]] = array[rows[i]-1,cols[i]-1]

        elif array[rows[i]+1,cols[i]-1] != Noval and rows[i]+1 <= no_rows and cols[i]-1 > 0:
        # give the cell the value of the cell that is at the left Top
            array[rows[i],cols[i]] = array[rows[i]+1,cols[i]-1]

        elif array[rows[i]+1,cols[i]+1] != Noval and rows[i]+1 <= no_rows and cols[i]+1 <= no_cols:
        # give the cell the value of the cell that is at the right Top
            array[rows[i],cols[i]] = array[rows[i]+1,cols[i]+1]
        #else:
            #print("the cell is isolated (No surrounding cells exist)")
    return array


def SaveRaster(raster,path): #ESTA FUNCIÓN ES IGUAL EN raster.py Y GISpy.py
    """
    ===================================================================
      SaveRaster(raster,path)
    ===================================================================
    this function saves a raster to a path

    inputs:
    ----------
        1- raster:
            [gdal object]
        2- path:
            [string] a path includng the name of the raster and extention like
            path="data/cropped.tif"

    Outputs:
    ----------
        the function does not return and data but only save the raster to the hard drive

    EX:
    ----------
        SaveRaster(raster,output_path)
    """
    #### input data validation
    # data type
    assert type(raster)==gdal.Dataset, "src should be read using gdal (gdal dataset please read it using gdal library) "
    assert type(path)== str, "Raster_path input should be string type"
    # input values
    ext=path[-4:]
    assert ext == ".tif", "please add the extension at the end of the path input"

    driver = gdal.GetDriverByName ( "GTiff" )
    dst_ds = driver.CreateCopy( path, raster, 0 )
    dst_ds = None # Flush the dataset to disk

#------------------------------

def align_parameter(dem, parameter_raster, output):
    
    DEM = gdal.Open(dem)
    raster = gdal.Open(parameter_raster)
    
    # align
    # aligned_raster = GIS.MatchRasterAlignment(DEM, raster)
    # dst_Aligned_M = GIS.MatchNoDataValue(DEM, aligned_raster)
    
    # TEST FUNCTIONS
    aligned_raster = MatchRasterAlignment(DEM, raster)
    read_align_raster = aligned_raster.ReadAsArray()
    print('El valor máximo del raster alineado es: {0}, y el valor mínimo es: {1}'.format(np.max(read_align_raster), np.min(read_align_raster)))
    dst_Aligned_M = MatchNoDataValue(DEM, aligned_raster)
    
    # save the new raster
    # GIS.SaveRaster(dst_Aligned_M, output)
    
    # TEST FUNCTIONS
    SaveRaster(dst_Aligned_M, output)
    
    DEM = None
    raster = None

for date in date_generated:
    
    fulldate = str(date.strftime("%Y.%m.%d"))
    
    #PRECIPITATION
    
    prec_input = input_raster_path + "prec/CHIRPS/P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + ".tif"
    prec_output = output_raster_path + "prec/P_CHIRPS.v2.0_mm-day-1_daily_" + fulldate + "_aligned.tif"
    align_parameter(dem_path, prec_input, prec_output)
    
    #EVAPOTRANSPIRATION
    
    evap_input = input_raster_path + "evap/ERA_INTERIM/Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + ".tif"
    evap_output = output_raster_path + "evap/Evaporation_ECMWF_ERA-Interim_mm_daily_" + fulldate + "_aligned.tif"
    align_parameter(dem_path, evap_input, evap_output)
    
    #TEMPERATURE

    temp_input = input_raster_path + "temp/ERA_INTERIM/Tair2m_ECMWF_ERA-Interim_C_daily_" + fulldate + ".tif"
    temp_output = output_raster_path + "temp/Tair2m_ECMWF_ERA-Interim_C_daily_" + fulldate + "_aligned.tif"
    align_parameter(dem_path, temp_input, temp_output)