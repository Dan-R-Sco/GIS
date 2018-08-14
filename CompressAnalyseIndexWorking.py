# Import system modules
import arcpy, os

# set workspace
workspace = r"Database Connections\Daniel@10.70.2.155.NDP_EGDB_20170105A.sde"

# set the workspace environment
arcpy.env.workspace = workspace

# No more users to connect to database
arcpy.AcceptConnections(workspace, False)

# Disconnect Users
arcpy.DisconnectUser(workspace, "ALL")

# Disconnect all users from the database.
arcpy.DisconnectUser('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde', "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
versionList = arcpy.ListVersions('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde')

# Execute the ReconcileVersions tool.
arcpy.ReconcileVersions_management('Database Connections/Daniel@10.70.2.155.NDP_EGDB_20170105A.sde', "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", r"C:/Users/daniel.scott/Desktop/log.txt")

# Compress database
arcpy.Compress_management(workspace)
print 'Compression Complete'

# Get a list of stand alone feature classes
dataList = arcpy.ListFeatureClasses()

# Add Feature classes in datasets
for dataset in arcpy.ListDatasets("", "Feature"):
    arcpy.env.workspace = os.path.join(workspace, dataset)
    dataList += arcpy.ListFeatureClasses()

# reset the workspace
arcpy.env.workspace = workspace

# Execute rebuild indexes
arcpy.RebuildIndexes_management(workspace, "SYSTEM", dataList, "ALL")
print 'Rebuild Complete'

# Execute analyse indexes
arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
print 'Analyze complete'

# Allow connections.
arcpy.AcceptConnections(workspace, True)