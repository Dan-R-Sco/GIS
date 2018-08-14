#script to rename fcs in a template dataset to remove the _1's

import arcpy
#input the db connection below i.e. r'Database Connections\User@server.sde
arcpy.env.workspace = <INPUT DB CONNECTION>
#List fc's that contain a key word
fclist = arcpy.ListFeatureClasses("","",<INPUT KEYWORD>)
for fc in fclist:
    if fc.endswith("_1"):
        newname = fc.replace('_1',"")
        arcpy.Rename_management(fc, newname)
    else:
        pass
