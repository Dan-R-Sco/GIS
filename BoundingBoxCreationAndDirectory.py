# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:47:43 2018

@author: daniel.scott
"""
#gdb_name = "DKRaster.gdb"
#ws = r"Q:\08_EXINT\01_KM\02_Projects\Search tool"
#gdbpath = os.path.join(ws, gdb_name)
import arcpy

file_name_field = 'FNAME'
input_gdb_or_folder = r'Q:\08_EXINT\01_KM\02_Projects\Search tool\V04_c.gdb'

arcpy.env.workspace = input_gdb_or_folder

#changed between arcpy.ListFeatureclasses() or Listrasters
feature_classes = arcpy.ListRasters()

for fc in feature_classes:
    print(fc) # just so you know what the script is processing
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