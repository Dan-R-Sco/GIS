""" 
Script that cycles through a current mxd and searches the source of each layer and replaces it with something else 

Inputs:
-Current MXD
-Find and Replace workspace paths
"""

import arcpy
mapdoc = arcpy.mapping.MapDocument("CURRENT")
mapdoc.findAndReplaceWorkspacePaths("<the directory you are changing from>" , "<the directory you are changing to>")
mapdoc.save()
del mapdoc
