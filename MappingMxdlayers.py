# -*- coding: utf-8 -*-

import arcpy, os

def write_log(text,file):
    f = open(file,'w')  #a appends to an existing file if it exists
    f.write("{}\n".format(text)) #write the text to the logfile and move to the next line
    return

output = r'X:\daniel.scott\V04.txt' #arcpy.GetParameterAsText(0)

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)

write_log("This report summarizes the names of all map documents and data frames within " + mxd.filePath +  "\n",output)
write_log("Date: " + str(datetime.datetime.today().strftime("%d %B, %Y")) + "\n",output)

for d in df:
    write_log("Data Frame: " + d.name, output)
    layers = arcpy.mapping.ListLayers(mxd, "", d)
    for lyr in layers:
        sizelist = []
        sumsize = sum(sizelist)
        print sumsize
        write_log("the sum of the number of files in your mxd is {0}".format(sumsize),output)
        try:
            lname = lyr.longName
            datasource = lyr.dataSource
            wspath = lyr.workspacePath
            write_log("Layer Name: " + lname, output)
            print "Layer Name: " + lname
            write_log("Data Source: " + datasource, output)
            print "Data Source: " + datasource
            write_log("Workspace Path: " + wspath,output)
            print "Workspace Path: " + wspath
        except:
            pass
    