# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:46:31 2018
identify duplicate layer names in mxd

Inputs:
-Current mxd

Outputs:
print in python module duplicate layer names
@author: daniel.scott
"""
import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT") # map document  
layers = arcpy.mapping.ListLayers(mxd) # list layers  
layer_set = dict() # create empty set  
for layer in layers: # loop through layers  
    if layer.name not in layer_set: # check if duplicate  
        layer_set[layer.name] = 1
        print layer.longName # or do something else  
    else: # if not duplicate  
        layer_set[layer.name] = layer_set[layer.name] + 1 # add to the set  

valid_kv = {k:v for k,v in layer_set.iteritems() if v > 2}
print valid_kv
