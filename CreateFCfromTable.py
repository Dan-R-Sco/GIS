# Name: CreateFeatureclass_Example2.py
# Description: Create a feature class to store the gnatcatcher habitat zones

# Import system modules
import arcpy

# Set workspace
arcpy.env.workspace = #insert connection 'W:\\XXX\\arcgis\\egdb\\Phase1\\ACQUIREFC\\XXXX'

views = [v for v in arcpy.ListTables() if v.endswith("_VW")]
# Set local variables
for table in views:
    print(view)
