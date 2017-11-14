import arcpy
mapdoc = arcpy.mapping.MapDocument("CURRENT")
mapdoc.findAndReplaceWorkspacePaths("<the directory you are changing from>" , "<the directory you are changing to>")
mapdoc.save()
del mapdoc