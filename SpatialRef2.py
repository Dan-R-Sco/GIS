import arcpy
from arcpy import env

mxd = arcpy.mapping.MapDocument("CURRENT")  # Uses your currently open MXD
df = arcpy.mapping.ListDataFrames(mxd, '')[0] # Chooses the first dataframe
layerlist = arcpy.mapping.ListLayers
env.workspace = 'c:/temp/python'

for layer in layerlist(mxd, '', df): # Loop through layers
    desc = arcpy.Describe(layer)
    sr = desc.spatialReference
    if sr.name == "Unknown":
        print layer + " has an unknown spatial reference\n"

        # Otherwise, print out the feature class name and
        #   spatial reference
    else:
        print layer.name + ": " + sr.name + "\n"
