
import arcpy, sets, os

gdb1 = arcpy.GetParameterAsText(0)
gdb2 = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)

print_list = []
outFile = open(output, "w")     

def print_domain_prop(domain):
    code_dict = {}
    write_it("\tCoded Values:")
    code_dict = domain.codedValues
    for key in code_dict.keys():
        write_it("\t\t" + str(key) + ": " + str(code_dict[key].encode("ascii", "ignore")))
    write_it("\tDomain Type: " + domain.domainType)
    write_it("\tRange: " + str(domain.range))
    write_it("\tField Type: " + domain.type)
    write_it("\tMerge Policy: " + domain.mergePolicy)
    write_it("\tSplit Policy: " + domain.splitPolicy)


def print_fld_prop(fld):
    write_it("\tType: " + fld.type)
    write_it("\tAlias: " + fld.aliasName)
    write_it("\tBase Name: " + fld.baseName)
    write_it("\tDomain: " + fld.domain)
    write_it("\tEditable: " + str(fld.editable))
    write_it("\tNullable: " + str(fld.isNullable))
    write_it("\tLength: " + str(fld.length))
    write_it("\tPrecision: " + str(fld.precision))
    write_it("\tRequired: " + str(fld.required))
    write_it("\tScale: " + str(fld.scale))


def print_fc_prop(fc):
    desc = arcpy.Describe(ws2 + os.sep + val)
    write_it("\tShape Type: " + desc.shapeType)
    write_it("\tShape Field Name: " + desc.shapeFieldName)
    write_it("\tSpatial Reference: " + desc.spatialReference.name)
    write_it("\tFeature Type: " + desc.featureType)
    write_it("\tHas M: " + str(desc.hasM))
    write_it("\tHas Z: " + str(desc.hasZ))
    write_it("\tHas Spatial Index: " + str(desc.hasSpatialIndex))


def print_list_domains(db, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Domains missing from " + db)
        for domain in list:
            write_it(domain.name)
            ##print_domain_prop(domain)
        write_it("\n")


def print_list_rcs(ws, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Relationship Classes missing from " + ws)
        for rc in list:
            write_it(rc)
        write_it("\n")


def print_list_fcs(ws1, ws2, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Feature Classes missing from " + ws1 + ":")
        for val in list:
            write_it(val)
            ##print_fc_prop(ws2 + os.sep + val)
        write_it("\n")


def print_list_flds(ws, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Fields missing from " + ws + ":")
        for val in list:
            write_it(val.name)
            ##print_fld_prop(val)
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
##            if feat_type == "Tables":
##                fldList = arcpy.ListFields(db + os.sep + diff)
##                write_it("Fields:")
##                for fld in fldList:
##                    write_it(fld.name)
##                    print_fld_prop(fld)
        write_it("\n")


def fc_diff(db, list1, list2, dict_name, dict_obj):
    diffList = set(list1) - set(list2)
    if len(diffList) > 0:
        write_it("*****************************************************************")
        write_it("Feature Classes missing from " + db + ":")
        for diff in diffList:
            write_it(diff)
            del dict_name[diff]
            del dict_obj[diff]
        write_it("\n")
    return dict_name, dict_obj


def process_fds(print_list):
    flds1 = []
    flds2 = []
    master_fcs = []
    master_flds = []
    fld_names1 = []
    fld_names2 = []
    dictFC1 = {}
    dictFC2 = {}
    dictRC1 = {}
    dictRC2 = {}
    dictFldsNames1 = {}
    dictFldsNames2 = {}
    dictFlds1 = {}
    dictFlds2 = {}

    arcpy.env.workspace = gdb1

    fdsList1 = arcpy.ListDatasets("", "Feature")
    for fds in fdsList1:
        fcList1 = arcpy.ListFeatureClasses("", "", fds)
        rcList1 = [rc.name for rc in arcpy.Describe(gdb1 + os.sep + fds).children if rc.datasetType == "RelationshipClass"]
        dictFC1[fds] = fcList1
        dictRC1[fds] = rcList1
            

    arcpy.env.workspace = gdb2

    fdsList2 = arcpy.ListDatasets("", "Feature")
    for fds in fdsList2:
        fcList2 = arcpy.ListFeatureClasses("", "", fds)
        rcList2 = [rc.name for rc in arcpy.Describe(gdb2 + os.sep + fds).children if rc.datasetType == "RelationshipClass"]
        dictFC2[fds] = fcList2
        dictRC2[fds] = rcList2


    # Compare Relationship Classes in common Feature Datasets only
    for key in dictRC1.keys():
        if not dictRC2.has_key(key):
            del dictRC1[key]

    for key in dictRC1.keys():
        rc1 = dictRC1[key]
        rc2 = dictRC2[key]
        rc1Diff = set(rc1) - set(rc2)
        rc2Diff = set(rc2) - set(rc1)
        for diff in rc2Diff:
            print_list.append(diff)
        print_list_rcs(gdb1 + os.sep + key, print_list)
        print_list = []
        for diff in rc1Diff:
            print_list.append(diff)
        print_list_rcs(gdb2 + os.sep + key, print_list)
        print_list = []
        


    # Compare Feature Classes common Feature Datasets only
    for key in dictFC1.keys():
        if not dictFC2.has_key(key):
            del dictFC1[key]


    for key in dictFC1.keys():
        val1 = dictFC1[key]
        val2 = dictFC2[key]
        master_fcs = sets.Set(val1 + val2)
        fcs1Diff = set(val1) - set(val2)
        fcs2Diff = set(val2) - set(val1)
        for diff in fcs2Diff:
            print_list.append(diff)
            master_fcs.remove(diff)
        print_list_fcs(gdb1 + os.sep + key, gdb2 + os.sep + key, print_list)
        print_list = []
        for diff in fcs1Diff:
            print_list.append(diff)
            master_fcs.remove(diff)
        print_list_fcs(gdb2 + os.sep + key, gdb1 + os.sep + key, print_list)
        print_list = []

        # Get fields from common Feature Classes
        for fc in master_fcs:
            fldsList1 = arcpy.ListFields(gdb1 + os.sep + key + os.sep + fc)
            for fld in fldsList1:
                flds1.append(fld)
                fld_names1.append(fld.name)
            dictFlds1[key + ":" + fc] = flds1
            dictFldsNames1[key + ":" + fc] = fld_names1
            flds1 = []
            fld_names1 = []
            fldsList2 = arcpy.ListFields(gdb2 + os.sep + key + os.sep + fc)
            for fld in fldsList2:
                flds2.append(fld)
                fld_names2.append(fld.name)
            dictFlds2[key + ":" + fc] = flds2
            dictFldsNames2[key + ":" + fc] = fld_names2
            fld_names2 = []
            flds2 = []
            
        master_fcs = []

    for key in dictFlds1.keys():
        fld_names1 = dictFldsNames1[key]
        fld_names2 = dictFldsNames2[key]
        fld_obj1 = dictFlds1[key]
        fld_obj2 = dictFlds2[key]
        parts = key.split(":")
        fds = parts[0]
        fc = parts[1]
        flds1Diff = set(fld_names1) - set(fld_names2)
        flds2Diff = set(fld_names2) - set(fld_names1)
        for diff in flds2Diff:
            for fld in fld_obj2:
                if fld.name == diff:
                    master_flds.append(fld)
        print_list_flds(gdb1 + os.sep + fds + os.sep + fc, master_flds)
        master_flds = []

        for diff in flds1Diff:
            for fld in fld_obj1:
                if fld.name == diff:
                    master_flds.append(fld)
        print_list_flds(gdb2 + os.sep + fds + os.sep + fc, master_flds)
        master_flds = []



#**********************************************************
# Main


#**********************************************************
# Workspace 1
arcpy.env.workspace = gdb1
gdb1DatasetList = arcpy.ListDatasets()
gdb1TableList = arcpy.ListTables()
gdb1FDSList = arcpy.ListDatasets("", "Feature")
gdb1RCList = [rc.name for rc in arcpy.Describe(gdb1).children if rc.datasetType == "RelationshipClass"]
gdb1FCList = arcpy.ListFeatureClasses()


#**********************************************************
# Get Fields in Stand-alone Feature Classes
flds_name1 = []
flds1 = []
dictFldName1 = {}
dictFlds1 = {}
for fc in gdb1FCList:
    fldList = arcpy.ListFields(fc)
    for fld in fldList:
        flds_name1.append(fld.name)
        flds1.append(fld)
    dictFldName1[fc] = flds_name1
    dictFlds1[fc] = flds1
    flds_name1 = []
    flds1 = []


#**********************************************************
# Workspace 2
arcpy.env.workspace = gdb2
gdb2DatasetList = arcpy.ListDatasets()
gdb2TableList = arcpy.ListTables()
gdb2RCList = [rc.name for rc in arcpy.Describe(gdb2).children if rc.datasetType == "RelationshipClass"]
gdb2FCList = arcpy.ListFeatureClasses()


#**********************************************************
# Get Fields in Stand-alone Feature Classes
flds_name2 = []
flds2 = []
dictFldName2 = {}
dictFlds2 = {}
for fc in gdb2FCList:
    fldList = arcpy.ListFields(fc)
    for fld in fldList:
        flds_name2.append(fld.name)
        flds2.append(fld)
    dictFldName2[fc] = flds_name2
    dictFlds2[fc] = flds2
    flds_name2 = []
    flds2 = []


#**********************************************************
# Compare Datasets
get_diff("Datasets", gdb1, gdb2DatasetList, gdb1DatasetList)
get_diff("Datasets", gdb2, gdb1DatasetList, gdb2DatasetList)


#**********************************************************
# Process data in Feature Datasets
process_fds(print_list)


#**********************************************************
# Compare Tables
get_diff("Tables", gdb1, gdb2TableList, gdb1TableList)
get_diff("Tables", gdb2, gdb1TableList, gdb2TableList)


#**********************************************************
# Compare Relationship Classes
get_diff("Relationship Classes", gdb1, gdb2RCList, gdb1RCList)
get_diff("Relationship Classes", gdb2, gdb1RCList, gdb2RCList)


#**********************************************************
# Compare Stand-alone Feature Classes
dictFldName2, dictFlds2 = fc_diff(gdb1, gdb2FCList, gdb1FCList, dictFldName2, dictFlds2)
dictFldName1, dictFlds1 = fc_diff(gdb2, gdb1FCList, gdb2FCList, dictFldName1, dictFlds1)


#**********************************************************
# Compare Fields of common Feature Classes
master_flds = []
for key in dictFldName1.keys():
    fld_names1 = dictFldName1[key]
    fld_names2 = dictFldName2[key]
    fld_obj1 = dictFlds1[key]
    fld_obj2 = dictFlds2[key]
    flds1Diff = set(fld_names1) - set(fld_names2)
    flds2Diff = set(fld_names2) - set(fld_names1)
    for diff in flds2Diff:
        for fld in fld_obj2:
            if fld.name == diff:
                master_flds.append(fld)
    print_list_flds(gdb1 + os.sep + key, master_flds)
    master_flds = []

    for diff in flds1Diff:
        for fld in fld_obj1:
            if fld.name == diff:
                master_flds.append(fld)
    print_list_flds(gdb2 + os.sep + key, master_flds)
    master_flds = []


#**********************************************************
# Compare Domains
master_domains = []
dmn_list1 = []
dmn_list2 = []
domains1 = arcpy.da.ListDomains(gdb1)
domains2 = arcpy.da.ListDomains(gdb2)
for d in domains1:
    dmn_list1.append(d.name)

for d in domains2:
    dmn_list2.append(d.name)

domain_diff1 = set(dmn_list1) - set(dmn_list2)
domain_diff2 = set(dmn_list2) - set(dmn_list1)

for diff in domain_diff2:
    for dmn in domains2:
        if dmn.name == diff:
            master_domains.append(dmn)
print_list_domains(gdb1, master_domains)
master_domains = []

for diff in domain_diff1:
    for dmn in domains1:
        if dmn.name == diff:
            master_domains.append(dmn)
print_list_domains(gdb2, master_domains)
master_domains = []

        


outFile.close()
arcpy.SetParameterAsText(3, output)
print "Done!"
