
import arcpy, sets, os

gdb = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

outFile = open(output, "w")
    


def print_domain_prop(domain):
    write_it(domain.name)
    code_dict = {}
    write_it("\tCoded Values:")
    code_dict = domain.codedValues
    if code_dict:
        for key in code_dict.keys():
            write_it("\t\t" + str(key) + ": " + str(code_dict[key].encode("ascii", "ignore")))
    write_it("\tDomain Type: " + domain.domainType)
    write_it("\tRange: " + str(domain.range))
    write_it("\tField Type: " + domain.type)
    write_it("\tMerge Policy: " + domain.mergePolicy)
    write_it("\tSplit Policy: " + domain.splitPolicy)   



def write_it(string):
    print string
    outFile.write(string + "\n")




#**********************************************************
# Main
domainList = arcpy.da.ListDomains(gdb)
for dmn in domainList:
    print_domain_prop(dmn)
    write_it("\n")


outFile.close()
arcpy.SetParameterAsText(2, output)
print "Done!"
