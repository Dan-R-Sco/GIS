# -*- coding: utf-8 -*-
"""
Created on Fri May 25 18:09:27 2018

@author: daniel.scott
"""

import os, arcpy, kitchen, re

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)

arcpy.env.workspace = "C:\Users\daniel.scott\Desktop\lyrtest"

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
                 pass

            else:
                #get layer name
                out_lyr = kitchen.text.converters.to_unicode(lyr.longName, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
                out_lyr = re.sub(r'[^\w]',"_", out_lyr)
                out_lyr = out_lyr + ".lyr"
                try:
                     #where to save the lyrs
                     lyrdir = r"C:\Users\daniel.scott\Desktop\lyrtest"
                     #check if table name is valid for creating a FC
                     try:
                         lyrtodo = os.path.join(lyrdir, out_lyr)
                         lyrtodo = "r" + '"' + lyrtodo + '"'
                         print lyrtodo
                         #create lyr file
                         arcpy.SaveToLayerFile_management(in_layer= lyr, out_layer= out_lyr, is_relative_path="", version="CURRENT")
                         #arcpy.SaveToLayerFile_management(lyr,lyrtodo)
                     except:
                         pass
                except:
                    arcpy.AddMessage(arcpy.GetMessages(2))
