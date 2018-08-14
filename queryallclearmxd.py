import arcpy

#Variables to form query syntax
#-------------------------------------------
#field in Attribute table
field = 'Source'
queryField = '"%s"' % field.strip()   #add double quotes field (for query syntax)
#value in specified field
value = "'Integrated Geological Map'"
#concatenate query syntax
queryStr = str(queryField) + "=" + str(value)
#--------------------------------------------
mxd = arcpy.mapping.MapDocument("CURRENT")

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DEFINITIONQUERY"):
        lyr.definitionQuery =""
arcpy.RefreshActiveView()
del mxd