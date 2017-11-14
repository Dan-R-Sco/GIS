
import arcpy, sets, os

gdb1 = arcpy.GetParameterAsText(0)
gdb2 = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)
compFlds = arcpy.GetParameterAsText(3)

print_list = []
outFile = open(output, "w")

def print_diff_prop(name, gdb1, gdb2, fc1, fc2, list):
    write_it("*****************************************************************")
    write_it(name + ":")
    write_it("Different properties: " + str(list))
    write_it("\n")
    write_it(gdb1 + ":")
    print_fc_prop(fc1)
    write_it("\n")
    write_it(gdb2 + ":")
    print_fc_prop(fc2)
    write_it("\n")


def compare_prop(prop1, prop2, flag, diff_list, prop):
    if prop1 != prop2:
        flag += 1
        diff_list.append(prop)
    return flag, diff_list


def print_fc_prop(desc):
    write_it("\tShape Type: " + desc.shapeType)
    write_it("\tShape Field Name: " + desc.shapeFieldName)
    write_it("\tFeature Type: " + desc.featureType)
    write_it("\tHas Spatial Index: " + str(desc.hasSpatialIndex))
    write_it("\tHas M: " + str(desc.hasM))
    write_it("\tHas Z: " + str(desc.hasZ))
    if compFlds:
        write_it("\tFields:")
        for fld in desc.fields:
            write_it("\t\t" + fld.name)



def print_list_fcs(db, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Feature Classes missing from " + db)
        for fc in list:
            write_it(fc)
        write_it("\n")       


def write_it(string):
    print string
    outFile.write(string + "\n")


def get_diff(feat_type, db, list1, list2):
    diffList = set(list1) - set(list2)
    if len(diffList) > 0:
        write_it("*****************************************************************")
        write_it(feat_type + " missing from " + db + ":")
        for diff in diffList:
            write_it(diff)
            list1.remove(diff)
        write_it("\n")
    return list1


def process_fds(print_list):
    dictFC1 = {}
    dictFC2 = {}
    rcNamesList1 = []
    rcNamesList2 = []

    arcpy.env.workspace = gdb1

    fdsList1 = arcpy.ListDatasets("", "Feature")
    for fds in fdsList1:
        fcList1 = arcpy.ListFeatureClasses("", "", fds)
        dictFC1[fds] = fcList1            


    arcpy.env.workspace = gdb2

    fdsList2 = arcpy.ListDatasets("", "Feature")
    for fds in fdsList2:
        fcList2 = arcpy.ListFeatureClasses("", "", fds)
        dictFC2[fds] = fcList2


    for key in dictFC1.keys():
        if not dictFC2.has_key(key):
            del dictFC1[key]


    for key in dictFC1.keys():
        fcs1 = dictFC1[key]
        fcs2 = dictFC2[key]
        fc1Diff = set(fcs1) - set(fcs2)
        fc2Diff = set(fcs2) - set(fcs1)
        for diff in fc2Diff:
            print_list.append(diff)
            fcs2.remove(diff)
        print_list_fcs(gdb1 + os.sep + key, print_list)
        print_list = []
        
        for diff in fc1Diff:
            print_list.append(diff)
            fcs1.remove(diff)
        print_list_fcs(gdb2 + os.sep + key, print_list)
        print_list = []


        # Compare properties of common Feature Classes in Common Feature Datasets
        flag = 0
        for fc1 in fcs1:
            diff_list = []
            fc_flds1 = []
            fc_flds2 = []
            for fc2 in fcs2:
                if fc1 == fc2:
                    desc1 = arcpy.Describe(gdb1 + os.sep + key + os.sep + fc1)
                    desc2 = arcpy.Describe(gdb2 + os.sep + key + os.sep + fc2)
                    flag, diff_list = compare_prop(desc1.featureType, desc2.featureType, flag, diff_list, "Feature Type")
                    flag, diff_list = compare_prop(desc1.hasM, desc2.hasM, flag, diff_list, "Has M")
                    flag, diff_list = compare_prop(desc1.hasZ, desc2.hasZ, flag, diff_list, "Has Z")
                    flag, diff_list = compare_prop(desc1.hasSpatialIndex, desc2.hasSpatialIndex, flag, diff_list, "Has Spatial Index")
                    flag, diff_list = compare_prop(desc1.shapeFieldName, desc2.shapeFieldName, flag, diff_list, "Shape Field Name")
                    flag, diff_list = compare_prop(desc1.shapeType, desc2.shapeType, flag, diff_list, "Shape Type")

                    fldsList1 = desc1.fields
                    fldsList2 = desc2.fields
                    for fld in fldsList1:
                        fc_flds1.append(fld.name)
                    fc_flds1.sort()
                    for fld in fldsList2:
                        fc_flds2.append(fld.name)
                    fc_flds2.sort()
                    if compFlds:
                        flag, diff_list = compare_prop(fc_flds1, fc_flds2, flag, diff_list, "Fields")
                if flag > 0:
                    print_diff_prop(fc1, gdb1 + os.sep + key, gdb2 + os.sep + key, desc1, desc2, diff_list)
                    flag = 0

        

#**********************************************************
# Main


#**********************************************************
# Get Feature Class lists for both geodatabases
arcpy.env.workspace = gdb1
gdb1FCList = arcpy.ListFeatureClasses()
arcpy.env.workspace = gdb2
gdb2FCList = arcpy.ListFeatureClasses()


#**********************************************************
# Process Feature Classes in Feature Datasets
process_fds(print_list)


#**********************************************************
# Compare Feature Classes
fcList2 = get_diff("Feature Classes", gdb1, gdb2FCList, gdb1FCList)
fcList1 = get_diff("Feature Classes", gdb2, gdb1FCList, gdb2FCList)


#**********************************************************
# Compare properties of common Feature Classes
flag = 0
for fc1 in fcList1:
    diff_list = []
    fc_flds1 = []
    fc_flds2 = []
    for fc2 in fcList2:
        if fc1 == fc2:
            desc1 = arcpy.Describe(gdb1 + os.sep + fc1)
            desc2 = arcpy.Describe(gdb2 + os.sep + fc2)
            flag, diff_list = compare_prop(desc1.featureType, desc2.featureType, flag, diff_list, "Feature Type")
            flag, diff_list = compare_prop(desc1.hasM, desc2.hasM, flag, diff_list, "Has M")
            flag, diff_list = compare_prop(desc1.hasZ, desc2.hasZ, flag, diff_list, "Has Z")
            flag, diff_list = compare_prop(desc1.hasSpatialIndex, desc2.hasSpatialIndex, flag, diff_list, "Has Spatial Index")
            flag, diff_list = compare_prop(desc1.shapeFieldName, desc2.shapeFieldName, flag, diff_list, "Shape Field Name")
            flag, diff_list = compare_prop(desc1.shapeType, desc2.shapeType, flag, diff_list, "Shape Type")

            fldsList1 = desc1.fields
            fldsList2 = desc2.fields
            for fld in fldsList1:
                fc_flds1.append(fld.name)
            fc_flds1.sort()
            for fld in fldsList2:
                fc_flds2.append(fld.name)
            fc_flds2.sort()
            if compFlds:
                flag, diff_list = compare_prop(fc_flds1, fc_flds2, flag, diff_list, "Fields")
        if flag > 0:
            print_diff_prop(fc1, gdb1, gdb2, desc1, desc2, diff_list)
            flag = 0

outFile.close()
arcpy.SetParameterAsText(4, output)
print "Done!"
