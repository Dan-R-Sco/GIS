# -*- coding: utf-8 -*-
"""
Created on Thu May 03 18:00:14 2018
create layer files for symbology
@author: daniel.scott
"""

import os, arcpy, kitchen

mxd = arcpy.mapping.MapDocument(r"G:\08_TiramisuProjects\W1612\Workspace\Consolidated GIS\TGTA_W1612_ConsolidatedGISPhase3_30Apr2018.mxd")
df = arcpy.mapping.ListDataFrames(mxd)

def write_log(text, log):
    f = open(log, 'w')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return
log = r"G:\08_TiramisuProjects\W1612\Workspace\lyrs.txt" 
ws = r"G:\08_TiramisuProjects\W1612\Workspace"

gdb_name = "RG_Handover.gdb"
gdbpath = os.path.join(ws, gdb_name)
for d in df:
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    # map layers 
    for lyr in layers:
        if lyr.supports("DATASOURCE"):
            if lyr.isRasterLayer:
                pass
            elif lyr.isGroupLayer == True:
                pass
            
            else:
                #get layer name
                newname = kitchen.text.converters.to_unicode(lyr.name, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
                lyr.name = newname
                lname = lyr.name
                #unicode the layer
                uni_name = kitchen.text.converters.to_unicode(lname, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
                datasource = lyr.dataSource
                try:
                    #where to save the lyrs
                    lyrdir = r"G:\08_TiramisuProjects\W1612\Workspace\Layers"
                    #check if table name is valid for creating a FC
                    try:
                        out_lyr = arcpy.ValidateTableName(uni_name)
                        lyrtodo = os.path.join(lyrdir, out_lyr)
                        #create lyr file
                        arcpy.SaveToLayerFile_management(lyr,lyrtodo)
                    except:
                        pass
                except:
                    arcpy.AddMessage(arcpy.GetMessages(2))
                    write_log(arcpy.GetMessages(2),log)