import arcpy
from arcpy import env


def write_log(text, file):
    f = open(file, 'a')  # a appends to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to the next line
    return


output = r'X:\daniel.scott\mxd6.txt'

mxd = arcpy.mapping.MapDocument("CURRENT")  # Uses your currently open MXD
df = arcpy.mapping.ListDataFrames(mxd, '')[0]  # Chooses the first dataframe

env.workspace = 'c:/temp/python'

# Create an output file
outFile = open(output, "w")
brknMXD = arcpy.mapping.ListBrokenDataSources(mxd)
layersskip = []
write_log("This report summarizes the names of all map documents and data frames within " + mxd.filePath + "\n", output)
write_log("Date: " + str(datetime.datetime.today().strftime("%d %B, %Y")) + "\n", output)

numbrklinks = 0

for brklayer in brknMXD:
    layersskip.append(brklayer)
    numbrklinks = numbrklinks + 1
    if numbrklinks == 1:
        write_log("***** Broken links found *****", output)
        write_log("Broken layer in the mxd : " + brklayer.name.encode(
            'utf-8') + " needs to have the source repaired or to be removed from the mxd", output)
    elif numbrklinks == 0:
        write_log("No broken layers found in the mxd, congratulations!", output)
    else:
        write_log("Broken layer in the mxd : " + brklayer.name.encode(
            'utf-8') + " needs to have the source repaired or to be removed from the mxd", output)

# Determine if the data source exists within the data frames/map document
for df in arcpy.mapping.ListDataFrames(mxd):
    layerlist = arcpy.mapping.ListLayers(mxd, '', df)
    write_log("", output)
    write_log(" Spatial relation analysis results: ", output)
    for layer in layerlist:
        if layer in brknMXD:
            pass
        elif layer.isGroupLayer:  # add code to count lyrs in this layer group
            descGroup = arcpy.Describe(layer)
            sublayernum = 0
            if sublayernum == 0:
                for subLayer in layer:
                    try:
                        desc = arcpy.Describe(subLayer)
                        srname = desc.spatialReference.name
                        if df.spatialReference.name == srname:
                            pass
                        # fails with layers with broken data sources
                        elif df.spatialReference.name != srname:
                            sublayernum = sublayernum + 1
                        if sublayernum == 1:
                            write_log(layer.name.encode('utf-8') + ' ' + " has layers inside with the wrong spatial projection:",output)
                            if srname == 'Unknown':
                                write_log('\t' + '\t' + subLayer.name.encode('utf-8') + " has an unknown spatial projection, you need to apply the correct spatial projection",output)
                            elif srname == None:
                                write_log('\t' + '\t' + subLayer.name.encode('utf-8') + ", doesn't have a spatial projection, how can this be used?", output)
                            else:
                                write_log('\t' + '\t' + subLayer.name.encode('utf-8') + " is being projected on the fly and will be affecting the mxd performance speed. The spatial reference: " + srname + " is being used, please reproject into the correct projection",output)
                    except:
                        pass
            if sublayernum != 0:
                for subLayer in layer:
                    try:
                        desc = arcpy.Describe(subLayer)
                        srname = desc.spatialReference.name
                        if df.spatialReference.name == srname:
                            pass
                        # fails with layers with broken data sources
                        elif df.spatialReference.name != srname:
                            if srname == 'Unknown':
                                write_log('\t' + '\t' + subLayer.name.encode('utf-8') + ", Layer name: " + subLayer.name.encode('utf-8') + " has an unknown spatial projection, you need to apply the correct spatial projection",output)
                            elif srname == None:
                                write_log('\t' + '\t' + subLayer.name.encode('utf-8') + ", doesn't have a spatial projection, how can this be used?", output)
                            else:
                                write_log('\t' + '\t' + subLayer.name.encode('utf-8') + " is being projected on the fly and will be affecting the mxd performance speed. The spatial reference: " + srname + " is being used, please reproject into the correct projection",output)
                    except:
                        pass
            pass