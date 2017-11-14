
import arcpy, sets, os

gdb1 = arcpy.GetParameterAsText(0)
gdb2 = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)
compFlds = arcpy.GetParameterAsText(3)

print_list = []
outFile = open(output, "w")

def print_diff_prop(table, gdb1, gdb2, desc1, desc2, list):
    write_it("*****************************************************************")
    write_it(table + ":")
    write_it("Different properties: " + str(list))
    write_it("\n")
    write_it(gdb1 + ":")
    print_table_prop(desc1)
    write_it("\n")
    write_it(gdb2 + ":")
    print_table_prop(desc2)
    write_it("\n")



def compare_prop(prop1, prop2, flag, diff_list, prop):
    if prop1 != prop2:
        flag += 1
        diff_list.append(prop)
    return flag, diff_list
    


def print_table_prop(table):
    write_it("\tHas OID: " + str(table.hasOID))
    write_it("\tOID Field Name: " + table.OIDFieldName)
    if compFlds:
        write_it("\tFields:")
        for fld in table.fields:
            write_it("\t\t" + fld.name)



def print_list_tables(db, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Tables missing from " + db)
        for table in list:
            write_it(table)
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




#**********************************************************
# Main


#**********************************************************
# Get Tables for both geodatabases
arcpy.env.workspace = gdb1
gdb1TableList = arcpy.ListTables()
arcpy.env.workspace = gdb2
gdb2TableList = arcpy.ListTables()


#**********************************************************
# Compare Tables
tableList1 = get_diff("Tables", gdb1, gdb2TableList, gdb1TableList)
tableList2 = get_diff("Tables", gdb2, gdb1TableList, gdb2TableList)


#**********************************************************
# Compare Values of Common Tables
flag = 0
for tbl1 in tableList1:
    diff_list = []
    table_fields1 = []
    table_fields2 = []
    for tbl2 in tableList2:
        if tbl1 == tbl2:
            desc1 = arcpy.Describe(gdb1 + os.sep + tbl1)
            desc2 = arcpy.Describe(gdb2 + os.sep + tbl2)
            flag, diff_list = compare_prop(desc1.hasOID, desc2.hasOID, flag, diff_list, "Has OID")
            flag, diff_list = compare_prop(desc1.OIDFieldName, desc2.OIDFieldName, flag, diff_list, "OID Field Name")

            fldsList1 = desc1.fields
            fldsList2 = desc2.fields
            for fld in fldsList1:
                table_fields1.append(fld.name)
            table_fields1.sort()
            for fld in fldsList2:
                table_fields2.append(fld.name)
            table_fields2.sort()
            if compFlds:
                flag, diff_list = compare_prop(table_fields1, table_fields2, flag, diff_list, "Fields")
        if flag > 0:
            print_diff_prop(tbl1, gdb1, gdb2, desc1, desc2, diff_list)
            flag = 0
        


outFile.close()
arcpy.SetParameterAsText(4, output)
print "Done!"
