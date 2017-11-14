import arcpy

# Set the workspace
arcpy.env.workspace = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_DVC.sde'

# Set a variable for the workspace
workspace = arcpy.env.workspace

connection = r'C:\Scripts_2016\Dans_Scripts\Connection\SDE@SRV-SQLHA02@CL_DVC.sde'

# Block new connections to the database.
#arcpy.AcceptConnections(connection, False) removed due to not working the accept

# Disconnect all users from the database.
arcpy.DisconnectUser(connection, "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
versionList = arcpy.ListVersions(connection)

# Execute the ReconcileVersions tool.
arcpy.ReconcileVersions_management(connection, "ALL_VERSIONS", "sde.QA", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", "C:\Scripts_2016\Dans_Scripts\Log.txt")

# Run the compress tool.
arcpy.Compress_management(connection)

# Allow the database to begin accepting connections again
#arcpy.AcceptConnections(connection, True)

# Get a list of datasets owned by the admin user

# Rebuild indexes and analyze the states and states_lineages system tables
arcpy.RebuildIndexes_management(workspace, "SYSTEM", "")

arcpy.AnalyzeDatasets_management(workspace, "SYSTEM","", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
