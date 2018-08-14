# -*- coding: utf-8 -*-
"""
Created on Wed May 02 12:11:03 2018
apply symbology
@author: daniel.scott
"""
# the MXDs to change, accessed and processed individually as 'i' is script not shown
import arcpy
mxd = arcpy.mapping.MapDocument(r'CURRENT')
for lyr in arcpy.mapping.ListLayers(mxd):
        arcpy.ApplySymbologyFromLayer_management(lyr,r"Q:\08_EXINT\01_KM\02_Projects\Search tool\Hollow.lyr")

mxd.saveACopy(r"Q:\08_EXINT\01_KM\02_Projects\Search tool\VectorIndex.mxd")
