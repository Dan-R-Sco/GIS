# -*- coding: utf-8 -*-
"""
Created on Thu May 03 16:25:54 2018
Mapping vectors in mxd to copy over into fgdb
@author: daniel.scott
"""
import os, arcpy, kitchen
def write_log(text, file):
    f = open(log, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return

mxd = arcpy.mapping.MapDocument(r"G:\08_TiramisuProjects\W1612\Workspace\Consolidated GIS\TGTA_W1612_ConsolidatedGISPhase3_30Apr2018.mxd")
df = arcpy.mapping.ListDataFrames(mxd)

#logfile
log = <INSERT LOGFILE> 

#Define workspace
ws = <INSERT WORKSPACE>
 
#define gdb to move data in
gdb_name = r"RG_handoverRastersDS.gdb"
gdbpath = os.path.join(ws, gdb_name)
rasterList = []
for d in df:
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    # map layers 
    for lyr in layers:
        if lyr.isGroupLayer:
            pass
        elif lyr.isRasterLayer:
            if lyr.supports("DATASOURCE"):
                #get layer name
                lname = kitchen.text.converters.to_unicode(lyr.name, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
                #unicode the layer
                lname = arcpy.ValidateTableName(lname)
                try:
                    #name of lyr in gdb
                    out_feature = os.path.join(gdbpath, lname)
                    #save to gdb
                    arcpy.arcpy.CopyRaster_management(lyr, out_feature)
                    msg = arcpy.AddMessage(arcpy.GetMessages())
                    write_log(msg,log)
                except:
                    try:
                        problem = arcpy.GetMessages()
                        arcpy.AddMessage(problem)
                        write_log("Failure with {}",log).format(problem)
                        pass
                    except:
                        pass
            else:
                try:
                    write_log("No data source for {}", log).format(arcpy.ValidateTableName(lyr.name))
                    pass
                except:
                    pass
        else:
            pass
