
import arcpy, sets, os

gdb = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

outFile = open(output, "w")


def print_rc_prop(rc):
    write_it(rc.name + ":")
    write_it("\tBackward Path Label: " + rc.backwardPathLabel)
    write_it("\tCardinality: " + rc.cardinality)
    write_it("\tClass Key: " + rc.classKey)
    write_it("\tDestination Class Names: " + str(rc.destinationClassNames))
    write_it("\tForward Path Label: " + rc.forwardPathLabel)
    write_it("\tAttachment Relationship: " + str(rc.isAttachmentRelationship))
    write_it("\tAttributed: " + str(rc.isAttributed))
    write_it("\tComposite: " + str(rc.isComposite))
    write_it("\tReflexive: " + str(rc.isReflexive))
    write_it("\tKey Type: " + rc.keyType)
    write_it("\tNotification: " + rc.notification)
    write_it("\tOrigin Class Names: " + str(rc.originClassNames))



def write_it(string):
    print string
    outFile.write(string + "\n")



#**********************************************************
# Main
rcList = [rc for rc in arcpy.Describe(gdb).children if rc.datasetType == "RelationshipClass"]
for rc in rcList:
    print_rc_prop(rc)
    write_it("\n")


outFile.close()
arcpy.SetParameterAsText(2, output)
print "Done!"
