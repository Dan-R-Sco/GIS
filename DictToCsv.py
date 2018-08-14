# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 17:30:45 2018
creates a file and writes the dictionary to the csv
approx. 15 mins for 10k records
@author: daniel.scott
"""

import csv
w = csv.writer(open(r"W:\daniel.scott\Search tool\output.csv", "w"))
for key, val in duplications.items(): #duplications here is a dictionary name
    w.writerow([key, val])