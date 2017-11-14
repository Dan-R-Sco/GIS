#import modules
import arcpy

#set workspace
arcpy.env.workspace = r"G:\04_ConfidentialData\ConfidentialProjects\ESAA\IC_E200\Data\Manifestation Extraction\Attribute Tables.gdb"

#set up a describe object for each fc in gdb
fcList = arcpy.ListFeatureClasses()
for fc in fcList:
    desc = arcpy.Describe(fc)
    print desc.spatialReference.name

print "Script completed"
