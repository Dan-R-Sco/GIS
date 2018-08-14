# -*- coding: utf-8 -*-
#Basic script to scan and walk from a path for the files and write to a log

import sys,os

def write_log(text, file):
    f = open(file, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return

logfile = <INPUT PATH AND TXT NAME>  # name of my log file
root = <INPUT THE FOLDER TO SEARCH>
for path, subdirs, files in os.walk(root):
    print path
    print subdirs
    print files
    for name in files:
        fullname = os.path.join(path, name)
        print(fullname)
        write_log(fullname, logfile)
