
import arcpy, sets, os

gdb1 = arcpy.GetParameterAsText(0)
gdb2 = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)

print_list = []
outFile = open(output, "w")

def print_diff_prop(gdb1, gdb2, dmn1, dmn2, list):
    write_it("*****************************************************************")
    write_it(dmn1.name + ":")
    write_it("Different properties: " + str(list))
    write_it("\n")
    write_it(gdb1 + ":")
    print_domain_prop(dmn1)
    write_it("\n")
    write_it(gdb2 + ":")
    print_domain_prop(dmn2)
    write_it("\n")



def compare_prop(prop1, prop2, flag, diff_list, prop):
    if prop1 != prop2:
        flag += 1
        diff_list.append(prop)
    return flag, diff_list
    


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



def print_list_domains(db, list):
    if len(list) > 0:
        write_it("*****************************************************************")
        write_it("Domains missing from " + db)
        for domain in list:
            write_it(domain.name)
            ##print_domain_prop(domain)
        write_it("\n")   



def write_it(string):
    print string
    outFile.write(string + "\n")




#**********************************************************
# Main


#**********************************************************
# Compare Domains
dmn_list1 = []
dmn_list2 = []
domains1 = arcpy.da.ListDomains(gdb1)
domains2 = arcpy.da.ListDomains(gdb2)
diffDomainsList = []
for d in domains1:
    dmn_list1.append(d.name)

for d in domains2:
    dmn_list2.append(d.name)

domain_diff1 = set(dmn_list1) - set(dmn_list2)
domain_diff2 = set(dmn_list2) - set(dmn_list1)

for diff in domain_diff2:
    for dmn in domains2:
        if dmn.name == diff:
            diffDomainsList.append(dmn)
            domains2.remove(dmn)
print_list_domains(gdb1, diffDomainsList)
diffDomainsList = []

for diff in domain_diff1:
    for dmn in domains1:
        if dmn.name == diff:
            diffDomainsList.append(dmn)
            domains1.remove(dmn)
print_list_domains(gdb2, diffDomainsList)
diffDomainsList = []


#**********************************************************
# Compare Values of Common Domains
flag = 0
for dmn1 in domains1:
    diff_list = []
    for dmn2 in domains2:
        if dmn1.name == dmn2.name:
            flag, diff_list = compare_prop(dmn1.codedValues, dmn2.codedValues, flag, diff_list, "Coded Values")
            flag, diff_list = compare_prop(dmn1.domainType, dmn2.domainType, flag, diff_list, "Domain Type")
            flag, diff_list = compare_prop(dmn1.range, dmn2.range, flag, diff_list, "Range")
            flag, diff_list = compare_prop(dmn1.type, dmn2.type, flag, diff_list, "Field Type")
            flag, diff_list = compare_prop(dmn1.mergePolicy, dmn2.mergePolicy, flag, diff_list, "Merge Policy")
            flag, diff_list = compare_prop(dmn1.splitPolicy, dmn2.splitPolicy, flag, diff_list, "Split Policy")
        if flag > 0:
            print_diff_prop(gdb1, gdb2, dmn1, dmn2, diff_list)
            flag = 0
        


outFile.close()
arcpy.SetParameterAsText(3, output)
print "Done!"
