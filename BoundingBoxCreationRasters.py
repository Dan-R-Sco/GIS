# -*- coding: utf-8 -*-
"""
Created on Mon May 07 14:36:39 2018
creates polygon feature of raster and creates fileds for name and directory, then it extends the polygon after recieving the coordinates from the raster. 
be careful that this inputs the infolder hardcoded and out folder
@author: daniel.scott
"""
import arcpy
infolder = r'Q:\08_EXINT\01_KM\02_Projects\Search tool\Raster.gdb'
out = r'Q:\08_EXINT\01_KM\02_Projects\Search tool\RasterBound.gdb'
arcpy.env.workspace = infolder
rasters = arcpy.ListRasters("*")

file_name_field = "RasterName"
file_dir_field = "RasterPath"

for raster in rasters:
    name = "Bounding_" + raster
    fc = arcpy.CreateFeatureclass_management(out,name,"POLYGON")
    arcpy.AddField_management(fc,file_name_field, "String","","",250)
    arcpy.AddField_management(fc,file_dir_field, "String","","",250)    
    r = arcpy.Raster(raster)
    point = arcpy.Point()
    array = arcpy.Array()
    corners = ["lowerLeft", "lowerRight", "upperRight", "upperLeft"]
    cursor = arcpy.InsertCursor(fc)
    feat = cursor.newRow()
    for corner in corners:    
        point.X = getattr(r.extent, "%s" % corner).X
        point.Y = getattr(r.extent, "%s" % corner).Y
        array.add(point)
    array.add(array.getObject(0))
    print len(array)
    polygon = arcpy.Polygon(array)
    feat.shape = polygon
    feat.setValue("RasterName", raster)
    feat.setValue("RasterPath", infolder)
    cursor.insertRow(feat)
    array.removeAll()
    del feat
    del cursor

