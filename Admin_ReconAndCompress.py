import arcpy

# set the workspace
## ie db connections\user@server@db
arcpy.env.workspace = <INPUT db conn>

# set a variable for the workspace
adminConn = arcpy.env.workspace

# block new connections to the database.
print("The database is no longer accepting connections")
arcpy.AcceptConnections(adminConn, False)

# disconnect all users from the database.
print("Disconnecting all users")

arcpy.DisconnectUser(adminConn, "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
print("Compiling a list of versions to reconcile")
versionList = arcpy.ListVersions(adminConn)
versionList = [ver.name for ver in verList if ver.parentVersionName == 'sde.DEFAULT']
# Execute the ReconcileVersions tool.
print("Reconciling all versions")

arcpy.ReconcileVersions_management((adminConn, "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT",
                                    "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION",
                                    "c:/temp/reconcilelog.txt")

# Run the compress tool.
try:
    if arcpy.Exists(adminConn):
    arcpy.Compress_management(adminConn)
    print "compressing"

# Allow the database to begin accepting connections again
print("Allow users to connect to the database again")
arcpy.AcceptConnections(adminConn, True)

# Update statistics and indexes for the system tables
# Note: to use the "SYSTEM" option the user must be an geodatabase or database administrator.
# Rebuild indexes on the system tables
print("Rebuilding indexes on the system tables")
arcpy.RebuildIndexes_management(adminConn, "SYSTEM")

# Update statistics on the system tables
print("Updating statistics on the system tables")
arcpy.AnalyzeDatasets_management(adminConn, "SYSTEM")

print("Finished.")
