
import arcpy, sets, os

ds = arcpy.GetParameterAsText(0)
flds = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)

outFile = open(output, "w")    


def print_fld_prop(fld):
    write_it(fld.name + ":")
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



def write_it(string):
    print string
    outFile.write(string + "\n")




#**********************************************************
# Main
##fldList = arcpy.ListFields(ds)
flds = flds.split(";")
fldList = arcpy.ListFields(ds)
for fld in fldList:
    for name in flds:
        if fld.name == name:
            print_fld_prop(fld)
            write_it("\n")


outFile.close()
arcpy.SetParameterAsText(3, output)
print "Done!"
