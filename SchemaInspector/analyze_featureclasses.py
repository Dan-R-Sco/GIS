
import arcpy, sets, os

gdb = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

outFile = open(output, "w")

def print_fc_prop(desc):
    write_it(desc.name + ":")
    write_it("\tShape Type: " + desc.shapeType)
    write_it("\tShape Field Name: " + desc.shapeFieldName)
    write_it("\tFeature Type: " + desc.featureType)
    write_it("\tHas Spatial Index: " + str(desc.hasSpatialIndex))
    write_it("\tHas M: " + str(desc.hasM))
    write_it("\tHas Z: " + str(desc.hasZ))



def write_it(string):
    print string
    outFile.write(string + "\n")

        

#**********************************************************
# Main
arcpy.env.workspace = gdb
fcList = arcpy.ListFeatureClasses()
for fc in fcList:
    desc = arcpy.Describe(fc)
    print_fc_prop(desc)
    write_it("\n")


outFile.close()
arcpy.SetParameterAsText(2, output)
print "Done!"
