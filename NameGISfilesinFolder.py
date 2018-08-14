# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 14:07:13 2018

@author: daniel.scott
"""
import arcpy, os, time

workspace = r"G:\08_TiramisuProjects\ICV04"
files = []

start = time.clock()

# Note that the files are limited to polygon feature classes
for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,datatype="FeatureClass",type='All'):
     for filename in filenames:
         files.append(os.path.join(dirpath, filename))


print "There are %s featureclasses in the workspace" % len(files)

end = time.clock()
total = end - start
print str(total) + " second to gather only feature classes"


#### for rasters
import arcpy, os, time
 
workspace = r"G:\08_TiramisuProjects\ICV04"
filesraster = []

start = time.clock()

# Note that the files are limited to polygon feature classes
for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,datatype=["RasterDataset","RasterCatalog","MosaicDataset","Terrain"],type='All'):
    for filename in filenames:
        filesraster.append(os.path.join(dirpath, filename))
print "There are %s rasters in the workspace" % len(filesraster)
end = time.clock()
total = end - start
print str(total) + " second to gather only rasters"