# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:48:33 2018
Script to be run in arc catalog. Select the MXD to run it over. Iterates through each layer in MXD and checks if that layer has data within the clip polygon, if it does,
it packages the data and moves it into a gdb. 

inputs: 
    mxd
    gdb
    clip polygon
    
writes the summary at the end of the run

approx running time 10s per vector lyr

-check if rasters works and find out how to get mxd entry to work, adding r' before the mapdoc input?

23/11/18 worked fully on orion. The get number of selection doesnt work, need to run a cleaning script afterwards
@author: daniel.scott
"""

import os, arcpy, kitchen
mapdoc= arcpy.GetParameterAsText(0)
mxd = arcpy.mapping.MapDocument(mapdoc)
df = arcpy.mapping.ListDataFrames(mxd)
ws = arcpy.GetParameterAsText(1)
clip_feature = arcpy.GetParameterAsText(2)

#C:\Users\daniel.scott\Documents\ArcGIS
#newmxd = arcpy.GetParameterAsText(3)

good_cnt = 0 
bad_cnt = 0
empty_cnt = 0
bad_lst = []
empty_lst = []
good_cntR = 0
bad_cntR = 0
bad_lstR = []

for lyr in arcpy.mapping.ListLayers(mxd, ""):
    longname = lyr.longName
    arcpy.AddMessage(longname)
    #print lyr
    arcpy.AddMessage(arcpy.GetMessages())
    if lyr.isGroupLayer:
        pass

    elif lyr.isRasterLayer:
        if lyr.supports("DATASOURCE"):
            #get layer name
            rname = kitchen.text.converters.to_unicode(longname, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
            #unicode the layer
            rname = arcpy.ValidateTableName(rname)
            try:
                #name of lyr in gdb
                out_feature = os.path.join(ws, rname)
                #clip layer and save to gdb
                # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
                ## Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
                arcpy.Clip_management(lyr,rectangle='#',out_raster=out_feature, in_template_dataset = clip_feature)
                good_cntR = good_cntR + 1
            except:
                bad_lstR.append(rname) 
                bad_cntR  = bad_cntR + 1
                pass
        else:
            bad_lstR.append(rname) 
            bad_cntR  = bad_cntR + 1
            pass
                
    else:
        try:
            if lyr.supports("DATASOURCE"):
                #get layer name
                lname = kitchen.text.converters.to_unicode(longname, encoding='utf-8', errors='replace', nonstring=None, non_string=None)
                #unicode the layer
                lname = arcpy.ValidateTableName(lname)
                encode = lname.encode('utf8', 'replace')
                arcpy.AddMessage(clip_feature)
                arcpy.SelectLayerByLocation_management(in_layer=lyr, overlap_type="INTERSECT", select_features=clip_feature)
                lyrpath = lyr.dataSource
                try:
                    matchcount = int(arcpy.GetCount_management('{0}'.format(lyrpath)).getOutput(0)) 
                    arcpy.AddMessage(str(matchcount)) 
                    print(matchcount)
                    if matchcount == 0:
                        empty_lst.append(encode)
                        empty_cnt = empty_cnt +1
                        pass

                
                    else:
                        if lyr.supports("DATASOURCE"):
                            try:
                                #name of lyr in gdb
                                out_feature = os.path.join(ws, lname)
                                #clip layer and save to gdb
                                print(arcpy.AddMessage("lyr is {0}, clip feat is {1} out feat is {2}".format(lyr, clip_feature, out_feature)))
                                #arcpy.Clip_analysis(in_features="General\south_border", clip_features="W:/daniel.scott/arcgis/Clip Example/clip_smallTest.gdb/Clip", out_feature_class="W:/daniel.scott/arcgis/Clip Example/clip_smallTest.gdb/cliptest", cluster_tolerance="")
                                lyrpath = lyr.dataSource
                                clippath = os.path.abspath(clip_feature)
                                arcpy.Clip_analysis(lyr, clip_feature, out_feature)
                                good_cnt = good_cnt + 1
                            except:
                                bad_cnt = bad_cnt + 1
                                bad_lst.append(encode)
                        else:
                            bad_cnt = bad_cnt + 1
                            bad_lst.append(encode)
                except:
                    arcpy.AddMessage("Get count failure") 
        except:
            bad_cnt = bad_cnt + 1
            bad_lst.append(encode)
                 
arcpy.AddMessage("Successfully clipped {0} features".format(str(good_cnt)))
arcpy.AddMessage("{0} features had no data inside the clip area".format(str(empty_cnt)))
arcpy.AddMessage("Could not clip {0} features".format(str(bad_cnt)))
arcpy.AddMessage("List of features unable to clip: ")
arcpy.AddMessage('\n'.join([feature for feature in bad_lst]))

arcpy.AddMessage("Successfully clipped {0} Rasters".format(str(good_cntR)))
arcpy.AddMessage("Could not clip {0} Rasters".format(str(bad_cntR)))
arcpy.AddMessage("List of Rasters unable to clip: ")
arcpy.AddMessage( '\n'.join([feature for feature in bad_lstR]))

""""
For mxd structure copying
#add group layer
groupLayer = arcpy.mapping.Layer(r"EmptyGroupLayer.lyr")
arcpy.mapping.AddLayer(dataFrame, groupLayer, "BOTTOM")

# add layer to group
AddLayerToGroup (data_frame, target_group_layer, add_layer, {add_position})
http://desktop.arcgis.com/en/arcmap/10.4/analyze/arcpy-mapping/addlayertogroup.htm


"""
