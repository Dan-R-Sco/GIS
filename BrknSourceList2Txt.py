# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:11:54 2018
brkn layer list creation to desktop as txt file, run in mxd
need to add question would you like to remove those broken links?
@author: daniel.scott
"""

import arcpy
import os
from arcpy import env

# set variables
mxd = arcpy.mapping.MapDocument("CURRENT")
#alternatively run this outside of the mxd and point to the mxd as below
#mxd = r'\\gisfile\GISmaps\AtlasMaps\ATLAS_MAPS_17\New folder'
fileloc = os.path.expanduser("~/Desktop/")
fileloc = fileloc.replace("\\","/")
fileloc = fileloc + "{}".format("BrkSrceLst.txt")
print fileloc
txtFile = open(fileloc, "w")
arcpy.overWriteOutputs = 1
# Write to text file
txtFile.write("MXDs that have broken source data" + "\n")
txtFile.write("----------------------------------------------" + "\n")
mapPath = mxd.filePath  
fileName = os.path.basename(mapPath)  
print fileName  
# iterates through folder and lists broken layers
txtFile.write("Checking " + fileName + "\n")
print "Checking " + fileName
for brknList in arcpy.mapping.ListBrokenDataSources(mxd):
    txtFile.write("\t broken layer: " + brknList.longName  + "\n")
    print "\t broken layer: " + brknList.longName
    # iterates through folder and checks for broken picture element source
    for elem in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT", "*logo*"):
        txtFile.write("\t broken picture element name: " + elem.name  + "\n")
        print "\t broken picture element name: " + elem.name
        txtFile.write("----" + fileName + " Completed----\n")
txtFile.write("----MXD Completed----")
txtFile.close()
