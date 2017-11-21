#renaming dataset and then FCs in edit still

import arcpy

arcpy.env.workspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'

outWorkspace = r'Database Connections\Dataowner@SRV-SQLHA02@DVC.sde'
print "Copying Template and writing Test "
arcpy.CopyFeatures_management("Template","Test")
