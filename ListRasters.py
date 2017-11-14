import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.isRasterLayer == True:
        print "raster layer: " + lyr.name + " Source: " + lyr.dataSource
            