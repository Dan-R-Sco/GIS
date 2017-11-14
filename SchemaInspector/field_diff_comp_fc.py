
import arcpy, sets, os

ds1 = arcpy.GetParameterAsText(0)
ds2 = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)

outFile = open(output, "w")

def print_diff_prop(ds1, ds2, fld1, fld2, list):
    write_it("*****************************************************************")
    write_it(fld1.name + ":")
    write_it("Different properties: " + str(list))
    write_it("\n")
    write_it(ds1 + ":")
    print_fld_prop(fld1)
    write_it("\n")
    write_it(ds2 + ":")
    print_fld_prop(fld2)
    write_it("\n")



def compare_prop(prop1, prop2, flag, diff_list, prop):
    if prop1 != prop2:
        flag += 1
        diff_list.append(prop)
    return flag, diff_list
    


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



def print_list_flds(ws, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Fields missing from " + ws + ":")
        for val in list:
            write_it(val.name)
        write_it("\n")     



def write_it(string):
    print string
    outFile.write(string + "\n")




#**********************************************************
# Main


#**********************************************************
# Compare Fields
fld_list1 = []
fld_list2 = []
flds1 = arcpy.ListFields(ds1)
flds2 = arcpy.ListFields(ds2)
diffFldsList = []
for fld in flds1:
    fld_list1.append(fld.name)

for fld in flds2:
    fld_list2.append(fld.name)

fld_diff1 = set(fld_list1) - set(fld_list2)
fld_diff2 = set(fld_list2) - set(fld_list1)

for diff in fld_diff2:
    for fld in flds2:
        if fld.name == diff:
            diffFldsList.append(fld)
            flds2.remove(fld)
print_list_flds(ds1, diffFldsList)
diffFldsList = []

for diff in fld_diff1:
    for fld in flds1:
        if fld.name == diff:
            diffFldsList.append(fld)
            flds1.remove(fld)
print_list_flds(ds2, diffFldsList)
diffFldsList = []


#**********************************************************
# Compare Values of Common Fields
flag = 0
for fld1 in flds1:
    diff_list = []
    for fld2 in flds2:
        if fld1.name == fld2.name:
            flag, diff_list = compare_prop(fld1.type, fld2.type, flag, diff_list, "Type")
            flag, diff_list = compare_prop(fld1.aliasName, fld2.aliasName, flag, diff_list, "Alias Type")
            flag, diff_list = compare_prop(fld1.baseName, fld2.baseName, flag, diff_list, "Base Name")
            flag, diff_list = compare_prop(fld1.domain, fld2.domain, flag, diff_list, "Domain")
            flag, diff_list = compare_prop(fld1.editable, fld2.editable, flag, diff_list, "Editable")
            flag, diff_list = compare_prop(fld1.isNullable, fld2.isNullable, flag, diff_list, "Nullable")
            flag, diff_list = compare_prop(fld1.length, fld2.length, flag, diff_list, "Length")
            flag, diff_list = compare_prop(fld1.precision, fld2.precision, flag, diff_list, "Precision")
            flag, diff_list = compare_prop(fld1.required, fld2.required, flag, diff_list, "Required")
            flag, diff_list = compare_prop(fld1.scale, fld2.scale, flag, diff_list, "Scale")
        if flag > 0:
            print_diff_prop(ds1, ds2, fld1, fld2, diff_list)
            flag = 0
        


outFile.close()
arcpy.SetParameterAsText(3, output)
print "Done!"
