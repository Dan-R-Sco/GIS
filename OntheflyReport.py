# -*- #################
"""
Created on Thu Apr 12 10:58:14 2018

@author: daniel.scott
"""

# Author:  ESRI
# Date:    July 5, 2010
# Version: ArcGIS 10.0
# Purpose: This script will iterate through each MXD in a folder and report the
#          name of each map document and data frame that has layers that are.
#          being projected on the fly.  The script is intended to run from a
#          script tool that requires two input parameters:
#               1) Folder containing MXDs,
#               2) An output text file.
#

import arcpy, datetime, os

try:

  #Read input parameters from GP dialog
  output = arcpy.GetParameterAsText(0)
  mxd = arcpy.mapping.MapDocument("CURRENT")
  #Create an output file
  outFile = open(output, "w")

  #Report header
  outFile.write("Data Source Report: \n")
  outFile.write("\n")
  outFile.write("This report summarizes the names of all map documents and data frames within \n")
  outFile.write("a folder that contain layers being projected on the fly. \n")
  outFile.write("\n")
  outFile.write("\n")
  outFile.write("Date: " + str(datetime.datetime.today().strftime("%B %d, %Y")) + "\n")
  outFile.write("----------------------------------------------------------------------------- \n")
  outFile.write(" MAPDOCUMENT: " + os.path.basename(mxd.filePath) + "\n")
  print(" MAPDOCUMENT: " + os.path.basename(mxd.filePath) + "\n")
  outFile.write("----------------------------------------------------------------------------- \n")

  #Loop through each MXD file
  mCnt = 0
  for df in arcpy.mapping.ListDataFrames(mxd):
      layerList = []
      for lyr in arcpy.mapping.ListLayers(mxd, "", df):                     
        if not lyr.isGroupLayer:
          try:
            desc = arcpy.Describe(lyr.dataSource) #fails with layers with broken data sources
            if desc and df.spatialReference.name != desc.spatialReference.name:
                mCnt = 1
                layerList.append(lyr.name)
            else:
                pass
          except:
              lyr = lyr.description
              outFile.write("\t\t Layer: " + lyr + " unable to assess" + "\n")
              print("\t\t Layer: " + lyr + " unable to assess" +"\n")
        else:
            lyr = lyr.description
            outFile.write("\t\t Group Layer Name: " + lyr + "\n")
      if len(layerList) > 0: #Write the data frame name once
        outFile.write("\n")
        outFile.write("\t Data Frame: " + df.name + "\n")
        for lyr in layerList: #Write each layer name
            lyr = unicode(lyr)
            if lyr.isRasterLayer:
                outFile.write("\n")
                outFile.write("\t\t RASTER PROJECTED ON THE FLY " + "Layer: " + lyr + " projected on the fly" + "\n")
            else:
                outFile.write("\t\t Layer: " + lyr + " projected on the fly" + "\n")
  outFile.write("Total of " + (layerList.count.encode('ascii', 'replace')) + " layers projected on the fly" + "\n")
  print("Total of " + str(layerList.count.encode('ascii', 'replace')) + " layers projected on the fly" + "\n")
  if mCnt == 0:
    outFile.write("\n")
    outFile.write("\n")
    outFile.write("--------------------------------------------------------------------------- \n")
    outFile.write("              NO PROJECTED ON THE FLY LAYERS FOUND \n")
    outFile.write("--------------------------------------------------------------------------- \n")
  outFile.close()


except Exception, e:
  import traceback
  map(arcpy.AddError, traceback.format_exc().split("\n"))
  arcpy.AddError(str(e))


