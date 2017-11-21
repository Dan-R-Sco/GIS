#renaming dataset and then FCs
import arcpy

arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'
currentname = arcpy.GetParameterAsText(0) #may need to add quotes to string
newname = arcpy.GetParameterAsText(1) #may need to add quotes to string
arcpy.Rename_management(currentname,newname)
fclist = arcpy.ListFeatureClasses("","",'newname') #may need to add quotes to string
for fc in fclist:
    print fc
    fcstripped = fc.lstrip('CL_DVC.OWD.') #strip the prefixe
    print fcstripped
    name = "CL_DVC.OWD." + newname + "_" + fcstripped #
    print name
    arcpy.Rename_management(fc, name)
