import arcpy

arcpy.env.workspace = r"Database Connections\\Daniel@srv-sql03@egdbA.sde"

fcList = []

for dataseti in arcpy.ListDatasets():
    for fc in arcpy.ListFeatureClasses("*", "ALL", dataseti):
        fcList.append(fc)

for fc in arcpy.ListFeatureClasses():
    fcList.append(fc)

print fcList