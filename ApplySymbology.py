# -*- coding: utf-8 -*-
"""
Created on Wed May 02 12:11:03 2018
apply symbology from a saved layer has to be used inside the mxd that you want to change the layer
@author: daniel.scott
"""
# the MXDs to change, accessed and processed individually as 'i' is script not shown
import arcpy
## input the symbol lyr to apply i.e. "C:\Docs\Hollow.lyr"
sym_to_apply = 
mxd = arcpy.mapping.MapDocument(r'CURRENT')
#cycle through lyrs in mxd and apply the symbology
for lyr in arcpy.mapping.ListLayers(mxd):
        arcpy.ApplySymbologyFromLayer_management(lyr, sym_to_apply)
#save the mxd
mxdsave_dest = r"C:\Docs\VectorIndex.mxd"
mxd.saveACopy(mxdsave_dest)
