
import arcpy, sets, os

gdb = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

outFile = open(output, "w")    


def print_table_prop(desc):
    write_it(desc.name + ":")
    write_it("\tHas OID: " + str(desc.hasOID))
    write_it("\tOID Field Name: " + desc.OIDFieldName)


def write_it(string):
    print string
    outFile.write(string + "\n")



#**********************************************************
# Main
arcpy.env.workspace = gdb
tableList = arcpy.ListTables()
for table in tableList:
    desc = arcpy.Describe(table)
    print_table_prop(desc)
    write_it("\n")



outFile.close()
arcpy.SetParameterAsText(2, output)
print "Done!"
