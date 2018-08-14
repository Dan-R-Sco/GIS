import arcpy, time, smtplib

# set the workspace
arcpy.env.workspace = 'Database Connections\Tool19@egdb_20170105A.sde'

# set a variable for the workspace
workspace = arcpy.env.workspace

# get a list of connected users.
userList = arcpy.ListUsers("Database Connections\Tool19@egdb_20170105A.sde")

#block new connections to the database.
arcpy.AcceptConnections('Database Connections\Tool19@egdb_20170105A.sde', False)

#disconnect all users from the database.
arcpy.DisconnectUser('Database Connections\Tool19@egdb_20170105A.sde', "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
versionList = arcpy.ListVersions('Database Connections\Tool19@egdb_20170105A.sde')

# Execute the ReconcileVersions tool.
arcpy.ReconcileVersions_management('Database Connections\Tool19@egdb_20170105A.sde', "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION", "c:\temp\reconcilelog.txt")

# Run the compress tool.
arcpy.Compress_management('Database Connections\Tool19@egdb_20170105A.sde')

#Allow the database to begin accepting connections again
arcpy.AcceptConnections('Database Connections\Tool19@egdb_20170105A.sde', True)

#Get a list of datasets owned by the admin user

# Get the user name for the workspace
# this assumes you are using database authentication.
# OS authentication connection files do not have a 'user' property.
userName = arcpy.Describe(arcpy.env.workspace).connectionProperties.user

# Get a list of all the datasets the user has access to.
# First, get all the stand alone tables, feature classes and rasters.
dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')

# Next, for feature datasets get all of the featureclasses
# from the list and add them to the master list.
for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
    dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)

# pass in the list of datasets owned by the admin to the rebuild indexes and analyze datasets tools
# Note: to use the "SYSTEM" option the user must be an administrator.
arcpy.RebuildIndexes_management(workspace, "SYSTEM", dataList, "ALL")

arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")