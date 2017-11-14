The SchemaInspector.tbx contains a suite of tools for analyzing components of a geodatabase and for finding the differences between geodatabase schemas.  The tools are grouped into three categories:
1. Analyzer Tools
2. Diff & Compare Tools
3. Diff Tools

There are five tools under the Analyzer Tools toolset.  These tools are for printing properties of a single geodatabase component.  Each tool has parameters for the input workspace and the output text file.
1. Analyze Domains
- Prints properties to a text file for each domain in a workspace including Domain Type, Range, Field Type, Merge Policy, and Split Policy.

2. Analyze Feature Classes
- Prints properties to a text file for each feature class in a workspace (geodatabase or feature dataset) including Shape Type, Shape Field Name, Feature Type, Spatial Index, Has M, and Has Z.

3. Analyze Fields
- Prints properties to a text file for each selected field in a feature class including Type, Alias, Base Name, Domain, Editable, Nullable, Length, Precision, Required, and Scale.

4. Analyze Relationship Classes
- Prints properties to a text file for each relationship class in a workspace including Backward Path Label, Cardinality, Class Key, Destination Class Names, Forward Path Label, Attachment Relationship, Attributed, Composite, Reflexive, Key Type, Notification, and Origin Class Names.

5. Analyze Tables
- Prints properties to a text file for each table in a workspace including Has OID and OID Field Name.


There are six tools under the Diff & Compare Tools toolset.  These tools are for comparing particular geodatabase components between two workspaces.  Each tool has parameters for the two schemas to compare and the output text file.
1. Domain Diff & Compare
- Prints the names of domains that are not common between workspaces to a text file.  Searches common domains and prints domain names and properties (same properties as the Analyze Domains tool) for domains with the same name but with different properties.

2. Feature Class Diff & Compare
- Prints the names of feature classes that are not common between workspaces to a text file.  Searches both standalone feature classes and feature classes in feature datasets.  Searches common feature classes and prints feature class names and properties (same properties as the Analyze Feature Classes tool) for feature classes with the same name but with different properties.

3. Field Diff & Compare (by Feature Class)
- Prints the names of fields that are not common between feature classes to a text file.  Searches common fields and prints field names and properties (same properties as the Analyze Fields tool) for fields with the same name but with different properties.

4. Field Diff & Compare (by Workspace)
- Prints the names of fields that are not common between all feature classes in the workspaces to a text file.  Searches both standalone feature classes and feature classes in feature datasets.  Searches common fields and prints field anmes and properties (same properties as the Analyze Fields tool) for fields with the same name but with different properties.

5. Relationship Class Diff & Compare
- Prints the names of relationship classes that are not common between workspaces to a text file.  Searches common relationship classes and prints relationship class names and properties (same properties as the Analyze Relationship Classes tool) for relationship classes with the same name but with different properties.

6. Table Diff & Compare
- Prints the names of tables that are not common between workspaces to a text file.  Searches common tables and prints table names and properties (same properties as the Analyze Tables tool) for tables with the same name but with different properties.


There is one tool under the Diff Tools toolset.  This tool combines all of the tools under Diff & Compare toolset into a single tool.  There are parameters for the two schemas to compare and the output text file.