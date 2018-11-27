# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 10:06:21 2018
Packaging base map extractor into arcGIS tool
User needs to input dest folder and 
@author: daniel.scott
"""


import arcpy
import time
# Modify the following path to change the folder were .jpg will be saved
destinationFolder = arcpy.GetParameterAsText(0)
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd,"Layers")[0]
fishnetLayer = arcpy.mapping.ListLayers(mxd,"fishnet",df)[0]
field = ["Id"] # field presente en el shapefile
with arcpy.da.SearchCursor(fishnetLayer,field) as cursor:
    for row in cursor:
        featureId = str(row[0])
        arcpy.SelectLayerByAttribute_management(fishnetLayer,
                                                "NEW_SELECTION",
                                                "\"Id\" = " + featureId)
        df.extent = fishnetLayer.getSelectedExtent(False)
        df.scale = df.scale * 1.1
        arcpy.SelectLayerByAttribute_management(fishnetLayer, "CLEAR_SELECTION")
        time.sleep(10)
        arcpy.mapping.ExportToJPEG(mxd,
                                   destinationFolder + "\\" + featureId + ".jpg",
                                   df,world_file = True,
                                   df_export_width = 1920,
                                   df_export_height = 1080)
        arcpy.RefreshActiveView()
del mxd
