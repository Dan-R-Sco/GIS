#renaming dataset and then FCs
import arcpy

arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'
currentname = arcpy.GetParameterAsText(0) #may need to add quotes to string
newname = arcpy.GetParameterAsText(1) #may need to add quotes to string
arcpy.Rename_management(currentname,newname)
fclist = arcpy.ListFeatureClasses("","",'newname') #may need to add quotes to string

for fc in fclist:
    if fc.endswith("_1"):
    newname = fc.replace('_1',"")
    arcpy.Rename_management(fc, newname)
else:
    pass