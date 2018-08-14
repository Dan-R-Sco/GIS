# -*- coding: utf-8 -*-
"""
Created on Thu May 03 16:47:00 2018
Mapping vectors in mxd and clipping to a new gdb
@author: daniel.scott
"""
import os, arcpy, kitchen
def write_log(text, file):
    f = open(log, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return

#Specify the map document
mxd = arcpy.mapping.MapDocument(<INSERT MAP DOCUMENT>")
df = arcpy.mapping.ListDataFrames(mxd)
#Specify the log file
log = r"G:\<LOG FILE>" 

#input workspace of where you are taking files 
ws = r"<WORKSPACE>"
                                
#GDB that you want to transfer files to
gdb_name = r"RG_HandoverVectors2.gdb"
gdbpath = os.path.join(ws, gdb_name)

#What is the clip area to be used?
clip_feature = <CLIP SHAPEFILE>
for d in df:
    layers = arcpy.mapping.ListLayers(mxd, "", d)
     # map layers 
    for lyr in layers:
         if lyr.isGroupLayer:
             pass
         elif lyr.isRasterLayer:
             pass
         else:
             if lyr.supports("DATASOURCE"):
                 #get layer name
                 lname = kitchen.text.converters.to_unicode(lyr.name, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
                 #unicode the layer
                 lname = arcpy.ValidateTableName(lname)
                 try:
                     #name of lyr in gdb
                     out_feature = os.path.join(gdbpath, lname)
                     #clip layer and save to gdb
                     arcpy.Clip_analysis(lyr, clip_feature, out_feature)
                     msg = arcpy.AddMessage(arcpy.GetMessages())
                     write_log(msg,log)
                 except:
                     try:
                         write_log("Failure with {}",log).format(lname)
                         pass
                     except:
                         pass
             else:
                 try:
                     write_log("No data source for {}", log).format(kitchen.text.converters.to_unicode(lyr.name, encoding='utf-8', errors='replace', nonstring=None, non_string=None))
                     pass
                 except:
                     pass
