
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


def print_rc_prop(rc):
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



def print_list_rcs(db, list):
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
    dictRC1 = {}
    dictRC2 = {}
    dictRCNames1 = {}
    dictRCNames2 = {}
    rcNamesList1 = []
    rcNamesList2 = []

    arcpy.env.workspace = gdb1

    fdsList1 = arcpy.ListDatasets("", "Feature")
    for fds in fdsList1:
        rcList1 = [rc for rc in arcpy.Describe(gdb1 + os.sep + fds).children if rc.datasetType == "RelationshipClass"]
        dictRC1[fds] = rcList1
        for rc in rcList1:
            rcNamesList1.append(rc.name)
        dictRCNames1[fds] = rcNamesList1
        rcNamesList1 = []
            

    arcpy.env.workspace = gdb2

    fdsList2 = arcpy.ListDatasets("", "Feature")
    for fds in fdsList2:
        rcList2 = [rc for rc in arcpy.Describe(gdb2 + os.sep + fds).children if rc.datasetType == "RelationshipClass"]
        dictRC2[fds] = rcList2
        for rc in rcList2:
            rcNamesList2.append(rc.name)
        dictRCNames2[fds] = rcNamesList2
        rcNamesList2 = []


    for key in dictRC1.keys():
        rc_names1 = dictRCNames1[key]
	if key in dictRCNames2:
	    rc_names2 = dictRCNames2[key]
            rc_obj1 = dictRC1[key]
            sameRCList1 = rc_obj1
            rc_obj2 = dictRC2[key]
            sameRCList2 = rc_obj2
            rc1Diff = set(rc_names1) - set(rc_names2)
            rc2Diff = set(rc_names2) - set(rc_names1)
            for diff in rc2Diff:
                for rc in rc_obj2:
                    if rc.name == diff:
                        print_list.append(rc)
                        sameRCList2.remove(rc)
            print_list_rcs(gdb1 + os.sep + key, print_list)
            print_list = []
        
            for diff in rc1Diff:
                for rc in rc_obj1:
                    if rc.name == diff:
                        print_list.append(rc)
                        sameRCList1.remove(rc)
            print_list_rcs(gdb2 + os.sep + key, print_list)
            print_list = []


            # Compare properties of common Relationship Classes in Common Feature Datasets
            flag = 0
            for rc1 in sameRCList1:
                diff_list = []
                for rc2 in sameRCList2:
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
                        print_diff_prop(gdb1 + os.sep + key, gdb2 + os.sep + key, rc1, rc2, diff_list)
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
