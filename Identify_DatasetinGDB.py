# A script to list list all fcs in all datasets in db
# Inputs:
# - workspace
# 

import arcpy

arcpy.env.workspace = r"Database Connections\\X@srv-sqlXX@XXX.sde"

fcList = []

for dataseti in arcpy.ListDatasets():
    for fc in arcpy.ListFeatureClasses("*", "ALL", dataseti):
        fcList.append(fc)

for fc in arcpy.ListFeatureClasses():
    fcList.append(fc)

print fcList
