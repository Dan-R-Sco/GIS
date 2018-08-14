# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:00:21 2018
script that changes the layer name to be FC name compatible (no spaces or special characters)
needs kitchen installed on computers
does not pick up some higher level group layers...unsure why
@author: daniel.scott
"""
import os, arcpy, kitchen, re

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)

#log = r"G:\08_TiramisuProjects\W1612\Workspace\lyrs.txt" 
#ws = r"G:\08_TiramisuProjects\W1612\Workspace"
count = 0
#gdb_name = "RG_Handover.gdb"
#gdbpath = os.path.join(ws, gdb_name)
for d in df:
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    # map layers 
    for lyr in layers:
        if lyr.supports("DATASOURCE"):
            if lyr.isRasterLayer:
                pass
            elif lyr.isGroupLayer == True:
                lyr.name = kitchen.text.converters.to_unicode(lyr.longName, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
                lyr.name = re.sub(r'[^\w]',"_", lyr.name)
                lyr.name = lyr.name.replace(" ","_")
                lyr.name = str(lyr.name)
                pass
            else:
                    #where to save the lyrs
                    #lyrdir = r"G:\08_TiramisuProjects\W1612\Workspace\Layers"
                    #check if table name is valid for creating a FC
                try:
                    out_lyr = kitchen.text.converters.to_unicode(lyr.name, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
                    out_lyr = re.sub(r'[^\w]',"_", out_lyr)
                    out_lyr = out_lyr.replace(" ","_")
                    print out_lyr + " changed to " + lyr.name
                    #lyrtodo = os.path.join(lyrdir, out_lyr)
                    if out_lyr != lyr.name:
                        count += 1
                        print "changed layer: {0} to {1}".format(lyr.name,out_lyr)
                        lyr.name = str(out_lyr)
                        #create lyr file
                        #arcpy.SaveToLayerFile_management(lyr,lyrtodo)
                    else:
                        pass
                except:
                    arcpy.AddMessage(arcpy.GetMessages(2))   
print "total number of layers with changed name {}".format(str(count))