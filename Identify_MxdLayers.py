# -*- coding: utf-8 -*-
"""
Created on Wed May 23 14:27:35 2018

Listing layers in mxd

inputs:
 - Current mxd
@author: daniel.scott
"""
import os, arcpy
 
# line 10 is used to create a list of main headers
#fdList = []
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)
for d in df:
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    for lyr in layers:
        if lyr.isGroupLayer == True:
            #add below to pull out only the main headers
            #if lyr.longName.find('\\') == -1:
            print lyr.name
            #fdList.append(lyr.longName)
        else:
            print("\t" + lyr.name)
