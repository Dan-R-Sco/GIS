# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 16:14:13 2018
removes fc's from gdb if they are empty
@author: daniel.scott
"""

import arcpy
from arcpy import env
env.workspace = arcpy.GetParameterAsText(0)

data_sets = arcpy.ListDatasets()

for item in data_sets:
    fcList = arcpy.ListFeatureClasses('', '', item)
    for item in fcList:
        fcLength = arcpy.GetCount_management(item)
        if int(fcLength.getOutput(0)) == 0:
            arcpy.Delete_management(item)
