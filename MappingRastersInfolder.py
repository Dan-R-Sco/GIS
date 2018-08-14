# -*- coding: utf-8 -*-
"""
Created on Wed May 02 11:15:22 2018
Script that walks through a folder, identifies rasters, checks if names are valid, copies to new gdb
and logs
@author: daniel.scott
"""

# -*- coding: utf-8 -*-

import os, arcpy, kitchen

def write_log(text, log):
    f = open(log, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return
#logfile definition
log = <INSERT LOG>
ws = <INPUT WORKSPACE>
gdb_name = "Raster.gdb"
gdbpath = os.path.join(ws, gdb_name)
#define which folder to check
root = <INSERT FOLDER>
walk = arcpy.da.Walk(root, topdown=True, datatype=["RasterDataset",'MosaicDataset'])  
rasterList = []
errors = []
for path, subdirs, files in walk:
    for file in files:
        raster = os.path.join(path, file)  
        rasterList.append(raster)
#created raster list and to check names
for raster in rasterList:
    try:
        path, file = os.path.split(raster)
        rastername = arcpy.ValidateTableName(file)
        kitchenrastername = kitchen.text.converters.to_unicode(rastername, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
        write_log("changed raster name from {0} to {1}".format(rastername,kitchenrastername),log)
        outraster = os.path.join(gdbpath,kitchenrastername)
        try:  
            arcpy.arcpy.CopyRaster_management(raster, outraster)
            write_log("Copied raster {}".format(kitchenrastername),log)
        except: 
            arcpy.AddMessage(arcpy.GetMessages(2))
            write_log(arcpy.GetMessages(2),log)
            pass
    except:
        print "error!! {}".format(rastername)
        errors.append(raster)
        pass

###Below used for mapping pilot folder in V04
import os, arcpy, kitchen
 
def write_log(text, log):
    f = open(log, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return
log = <DEFINE LOG TXT FILE>
#define ws can be a folder
ws = <INSERT WORKSPACE>
gdb_name = "Raster.gdb"
gdbpath = os.path.join(ws, gdb_name)

#Define where to search for the rasters
root = <Folder to search in>
walk = arcpy.da.Walk(root, topdown=True, datatype=["RasterDataset",'MosaicDataset'])  
rasterList = []
errors = []
for path, subdirs, files in walk:
    for file in files:
        raster = os.path.join(path, file)  
        rasterList.append(raster)
#created raster list and to check names
for raster in rasterList:
    try:
        path, file = os.path.split(raster)
        basename, ext = os.path.splitext(file)
        rastername = arcpy.ValidateTableName(basename)
        kitchenrastername = kitchen.text.converters.to_unicode(rastername, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
        outraster = os.path.join(gdbpath,kitchenrastername)
        try:  
            arcpy.arcpy.CopyRaster_management(raster, outraster)
            write_log(arcpy.GetMessages(0),log)
        except: 
            write_log(arcpy.GetMessages(2),log)
            pass
    except:
        try:
            errors.append(raster)
            pass
        except:
            pass
