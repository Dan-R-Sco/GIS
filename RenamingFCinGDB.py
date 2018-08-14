# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:58:06 2018

@author: daniel.scott
"""

import arcpy, sys, os

arcpy.env.workspace =  r'Q:\08_EXINT\01_KM\02_Projects\Search tool\V04.gdb'
fcs = arcpy.ListFeatureClasses()
arcpy.AddMessage("Listing FCs in dataset: ")
for fc in fcs:
    if fc.startswith("CL_"):
        newname = fc.replace("CL_","")
        arcpy.Rename_management(fc,newname)
    else:
        continue
    if fc.startswith("V04"):
        pass
    else:
        newname = "V04_" + fc
        arcpy.AddMessage("Renaming fc {0} to {1})".format(fc,newname))
        arcpy.Rename_management(fc,newname)

