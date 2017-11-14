#import modules
import arcpy

#set workspace
arcpy.env.workspace = r"G:\XXXX.gdb"

#set up a describe object for each fc in gdb
fcList = arcpy.ListFeatureClasses()
for fc in fcList:
    desc = arcpy.Describe(fc)
    print desc.spatialReference.name

print "Script completed"
