# Name: CreateFeatureclass_Example2.py
# Description: Create a feature class to store the gnatcatcher habitat zones

# Import system modules
import arcpy

# Set workspace
arcpy.env.workspace = 'W:\\daniel.scott\\arcgis\\egdb\\Phase1\\ACQUIREFC\\dataowner@SRV-SQLHA02.sde'

views = [v for v in arcpy.ListTables() if v.endswith("_VW")]
# Set local variables
for table in views:
    print(view)
