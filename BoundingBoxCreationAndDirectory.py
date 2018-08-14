# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:47:43 2018
Checks raster inside a gdb and creates bounding boxes for them.
Creates new field in bounding box fc and writes the original fc name as an attribute
@author: daniel.scott
"""

import arcpy

file_name_field = 'FNAME'
##input gdb i.e. r'Q:\test.gdb'
input_gdb_or_folder = 

arcpy.env.workspace = input_gdb_or_folder

#changed between arcpy.ListFeatureclasses() or Listrasters
feature_classes = arcpy.ListRasters()

for fc in feature_classes:
    ##Ensure that the raster file is not corrupt
    try:
        arcpy.RepairGeometry_management(fc)
    except:
        pass
    print(fc) # just so you know what the script is processing
    #Create new fc for each bounding box
    outFeatureClass = "Bounding_" + fc
    try:
        arcpy.MinimumBoundingGeometry_management(fc, outFeatureClass,"RECTANGLE_BY_AREA", "ALL")
        # add field to hold the file name if it does not exist
        existing_fields = [f.name for f in arcpy.ListFields(outFeatureClass)]
        if file_name_field not in existing_fields:
            arcpy.management.AddField(outFeatureClass, file_name_field, 'TEXT', field_length=200)
        # write the file name into each row of the file name filed
        with arcpy.da.UpdateCursor(outFeatureClass, [file_name_field]) as uc:
            for row in uc:
                uc.updateRow([input_gdb_or_folder + "\\" + str(fc)])
        del row, uc
    except:
        print "unable to process: "
        print fc
