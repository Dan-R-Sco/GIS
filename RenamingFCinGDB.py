# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:58:06 2018

@author: daniel.scott
"""

import arcpy, sys, os

#define the gdb
arcpy.env.workspace =  <DIRECTORY TO THE GDB INCLUDING THE GDB EXTENSION>
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
        #Define prefix wanted below
        newname = "V04_" + fc
        arcpy.AddMessage("Renaming fc {0} to {1})".format(fc,newname))
        arcpy.Rename_management(fc,newname)

###For those inside a dataset
import arcpy, sys, os

 #define the gdb
arcpy.env.workspace = <database connection including dataset path>
fcs = arcpy.ListFeatureClasses()
arcpy.AddMessage("Listing FCs in dataset: ")
for fc in fcs:
    newname = fc.replace(<DB.USER.>,"DB.USER.ProjName_")
    arcpy.Rename_management(fc,newname)
