# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 09:32:01 2018
Script that will iterate through the layers in a map document and copy each layer into a gdb
@author: daniel.scott
"""

import os, arcpy, unidecode
 
 
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)
 
#workspace where the gdb will be placed
ws = <ENTER DIRECTORY>
#Enter gdb name
gdb_name = "Project1.gdb"
 
 #create gdb
arcpy.CreateFileGDB_management(ws, gdb_name)
print("Created GDB successfully")
 
gdbpath = os.path.join(ws, gdb_name)
 
for d in df:
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    for lyr in layers:
        try:
            lname = lyr.name
            uni_name = unidecode.unidecode(lname)
            datasource = lyr.dataSource
            if lyr.isRasterLayer:
                print(uni_name + " is a raster layer and will not be transferred")
            arcpy.FeatureClassToFeatureClass_conversion(datasource,gdbpath,uni_name)
            print datasource + " copied to EGDB as " + uni_name 
             
             
        except:
            if lyr.isGroupLayer == True:
                print str(lyr) + " is a group header therefore cannot be converted"
            else:
                try:
                    print "Unable to convert: " + str(datasource)
                except:
                    print "Unable to convert: " + str(lname)
