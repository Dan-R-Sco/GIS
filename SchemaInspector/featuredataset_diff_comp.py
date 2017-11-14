
import arcpy, sets, os

gdb1 = arcpy.GetParameterAsText(0)
gdb2 = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)

print_list = []
outFile = open(output, "w")

def print_diff_prop(gdb1, gdb2, rc1, rc2, list):
    write_it("*****************************************************************")
    write_it(rc1.name + ":")
    write_it("Different properties: " + str(list))
    write_it("\n")
    write_it(gdb1 + ":")
    print_rc_prop(rc1)
    write_it("\n")
    write_it(gdb2 + ":")
    print_rc_prop(rc2)
    write_it("\n")


def compare_prop(prop1, prop2, flag, diff_list, prop):
    if prop1 != prop2:
        flag += 1
        diff_list.append(prop)
    return flag, diff_list


def print_fds_prop(desc):
    code_dict = {}
    write_it("\tSpatial Reference: " + desc.spatialReference)
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



def print_list_fds(db, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Relationship Classes missing from " + db)
        for rc in list:
            write_it(rc.name)
            ##print_rc_prop(rc)
        write_it("\n")       


def write_it(string):
    print string
    outFile.write(string + "\n")


def get_diff(feat_type, db, list1, list2):
    names1 = []
    names2 = []
    for rc in list1:
        names1.append(rc.name)
    for rc in list2:
        names2.append(rc.name)
    diffList = set(names1) - set(names2)
    if len(diffList) > 0:
        write_it("*****************************************************************")
        write_it(feat_type + " missing from " + db + ":")
        for diff in diffList:
            write_it(diff)
            for rc in list1:
                if rc.name == diff:
                    list1.remove(rc)
        write_it("\n")
    return list1


def process_fds(print_list):
    arcpy.env.workspace = gdb1
    fdsList1 = arcpy.ListDatasets("", "Feature")
    sameFDSList1 = fdsList1

    arcpy.env.workspace = gdb2
    fdsList2 = arcpy.ListDatasets("", "Feature")
    sameFDSList2 = fdsList2


    fdsDiff1 = set(fdsList1) - set(fdsList2)
    fdsDiff2 = set(fdsList2) - set(fdsList1)
    for fds in fdsDiff2:
        print_list.append(fds)
        sameFDSList2.remove(fds)
    print_list_fds(gdb1, print_list)
    print_list = []

    for fds in fdsDiff1:
        print_list.append(fds)
        sameFDSList1.remove(fds)
    print_list_fds(gdb2, print_list)
    print_list = []
        


    # Compare properties of common Feature Datasets
    flag = 0
    for fds1 in sameFDSList1:
        diff_list = []
        for fds2 in sameFDSList2:
            if fds1 == fds2:
                desc1 = arcpy.Describe(gdb1 + os.sep + fds1)
                desc2 = arcpy.Describe(gdb2 + os.sep + fds2)
                flag, diff_list = compare_prop(desc1.spatialReference.name, desc2.spatialReference.name, flag, diff_list, "Spatial Reference")            
                flag, diff_list = compare_prop(desc1.canVersion, desc2.canVersion, flag, diff_list, "Can Version")
                flag, diff_list = compare_prop(desc1.isVersioned, desc2.isVersioned, flag, diff_list, "Is Versioned")        
                flag, diff_list = compare_prop(desc1.DSID, desc2.DSID, flag, diff_list, "DSID")
                flag, diff_list = compare_prop(desc1.mExtent, desc2.mExtent, flag, diff_list, "M Extent")
                flag, diff_list = compare_prop(desc1.zExtent, desc2.zExtent, flag, diff_list, "Z Extent")
            if flag > 0:
                print_diff_prop(gdb1, gdb2, desc1, desc2, diff_list)
                flag = 0

        

#**********************************************************
# Main


#**********************************************************
# Compare Relationship Classes
gdb1RCList = [rc for rc in arcpy.Describe(gdb1).children if rc.datasetType == "RelationshipClass"]
gdb2RCList = [rc for rc in arcpy.Describe(gdb2).children if rc.datasetType == "RelationshipClass"]


#**********************************************************
# Process Relationship Classes in Feature Datasets
process_fds(print_list)


#**********************************************************
# Compare Relationship Classes
rcList2 = get_diff("Relationship Classes", gdb1, gdb2RCList, gdb1RCList)
rcList1 = get_diff("Relationship Classes", gdb2, gdb1RCList, gdb2RCList)


#**********************************************************
# Compare properties of common Relationship Classes
flag = 0
for rc1 in rcList1:
    diff_list = []
    for rc2 in rcList2:
        if rc1.name == rc2.name:
            flag, diff_list = compare_prop(rc1.backwardPathLabel, rc2.backwardPathLabel, flag, diff_list, "Backward Path Label")
            flag, diff_list = compare_prop(rc1.cardinality, rc2.cardinality, flag, diff_list, "Cardinality")
            flag, diff_list = compare_prop(rc1.classKey, rc2.classKey, flag, diff_list, "Class Key")
            flag, diff_list = compare_prop(rc1.destinationClassNames, rc2.destinationClassNames, flag, diff_list, "Destination Classes")
            flag, diff_list = compare_prop(rc1.forwardPathLabel, rc2.forwardPathLabel, flag, diff_list, "Forward Path Label")
            flag, diff_list = compare_prop(rc1.isAttachmentRelationship, rc2.isAttachmentRelationship, flag, diff_list, "Attachment Relationship")
            flag, diff_list = compare_prop(rc1.isAttributed, rc2.isAttributed, flag, diff_list, "Attributes")
            flag, diff_list = compare_prop(rc1.isComposite, rc2.isComposite, flag, diff_list, "Composite")
            flag, diff_list = compare_prop(rc1.isReflexive, rc2.isReflexive, flag, diff_list, "Reflexive")
            flag, diff_list = compare_prop(rc1.keyType, rc2.keyType, flag, diff_list, "Key Type")
            flag, diff_list = compare_prop(rc1.notification, rc2.notification, flag, diff_list, "Notification")
            flag, diff_list = compare_prop(rc1.originClassNames, rc2.originClassNames, flag, diff_list, "Origin Classes")
        if flag > 0:
            print_diff_prop(gdb1, gdb2, rc1, rc2, diff_list)
            flag = 0        


outFile.close()
arcpy.SetParameterAsText(3, output)
print "Done!"
