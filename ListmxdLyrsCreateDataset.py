# -*- coding: utf-8 -*-
"""
Created on Wed May 23 17:49:19 2018
list mxd headers and create dataset
@author: daniel.scott
"""

import arcpy, os
mxd = arcpy.mapping.MapDocument("CURRENT")

fdList = []

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.isGroupLayer == True:
        if lyr.longName.find('\\') == -1:
            print lyr.longName
            fdList.append(lyr.longName)

arcpy.env.overwriteOutput = True

folList = ["D:\\GIS_Temp\Folder A", "D:\\GIS_Temp\\Folder B", "D:\\GIS_Temp\\Folder C"]

workRange = range(len(fdList))

for thisIndex in workRange:
    fd = fdList[thisIndex]
    arcpy.env.workspace = folList[thisIndex]
    arcpy.CreateFeatureDataset_management("D:\\GIS_Temp\\TEST.gdb", fd, "D:\\GIS_Temp\\Projection.prj")

    for impFC in arcpy.ListFeatureClasses():
        fcName,fcExt = os.path.splitext(impFC)
        fcName.replace(" ","_")
        arcpy.FeatureClassToFeatureClass_conversion( os.path.join(folList[thisIndex], impFC), os.path.join("D:\\GIS_Temp\\TEST.gdb", fd), fcName)
        
        
        
"""
The question posed these as the outputs
https://gis.stackexchange.com/questions/191477/create-feature-datasets-from-group-layer-name

arcpy.env.overwriteOutput = True
    fdList  = ["Dataset_A", "Dataset_B", "Dataset_C"]
    folList = ["D:\\GIS_Temp\Folder A", "D:\\GIS_Temp\\Folder B", "D:\\GIS_Temp\\Folder C"]
    workRange = range(len(fdList))
    for thisIndex in workRange:
        fd = fdList[thisIndex]
        arcpy.env.workspace = folList[thisIndex]
        arcpy.CreateFeatureDataset_management("D:\\GIS_Temp\\TEST.gdb", fd, "D:\\GIS_Temp\\Projection.prj")
        for impFC in arcpy.ListFeatureClasses():
            fcName,fcExt = os.path.splitext(impFC)
            fcName.replace(" ","_")
            arcpy.FeatureClassToFeatureClass_conversion(os.path.join(folList[thisIndex],impFC),os.path.join("D:\\GIS_Temp\\TEST.gdb",fd),fcName)"""