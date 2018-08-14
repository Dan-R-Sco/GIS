# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:09:20 2018
script to change data source
@author: daniel.scott
"""

import arcpy  
mxd = arcpy.mapping.MapDocument(r"C:\Project\Project.mxd")  
mxd.findAndReplaceWorkspacePaths(r"C:\Project\Data", r"C:\Project\Data2")  
mxd.saveACopy(r"C:\Project\Project2.mxd")  
del mxd