#script to rename fcs in a template dataset to remove the _1's

import arcpy

arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'

fclist = arcpy.ListFeatureClasses("","",'W1709')
for fc in fclist:
    if fc.endswith("_1"):
        newname = fc.replace('_1',"")
        arcpy.Rename_management(fc, newname)
    else:
        pass