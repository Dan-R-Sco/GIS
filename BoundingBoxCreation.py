# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:14:44 2018
Script to create bounding boxes to FCs held in a gdb
@author: daniel.scott
"""
import arcpy
arcpy.env.workspace = r'Q:\08_EXINT\01_KM\02_Projects\Search tool\V04.gdb'
fcs = arcpy.ListFeatureClasses()
arcpy.AddMessage("Collecting Fcs ")

for fc in fcs:
    try:
        arcpy.RepairGeometry_management(fc)
    except:
        pass
    try:
        #create name of FC to be created
        newname = "Bounding_" + fc
        arcpy.AddMessage("Creating the output FC {0})".format(newname, fc))
        #add gdb directory to output
        outfc = newname
        #create bounding box
        arcpy.MinimumBoundingGeometry_management(fc, outfc, "CONVEX_HULL", "ALL")
    except:
        pass