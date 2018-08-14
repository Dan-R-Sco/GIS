import arcpy

#Variables to form query syntax
#-------------------------------------------
#field in Attribute table
field = 'Source'
queryField = '"%s"' % field.strip()   #add double quotes field (for query syntax)
#value in specified field
value = "'Cadastre of ore deposits Antofagasta'"
#concatenate query syntax
queryStr = str(queryField) + "=" + str(value)
#--------------------------------------------
mxd = arcpy.mapping.MapDocument("CURRENT")

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DEFINITIONQUERY"):
        lyr.definitionQuery = queryStr
arcpy.RefreshActiveView()
del mxd