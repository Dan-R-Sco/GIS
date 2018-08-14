# -*- coding: utf-8 -*-

import sys,os

def write_log(text, file):
    f = open(file, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return

logfile = r"X:\daniel.scott\V04log2.txt"  # name of my log file
root = r"G://08_TiramisuProjects//ICV04"
for path, subdirs, files in os.walk(root):
    print path
    print subdirs
    print files
    for name in files:
        fullname = os.path.join(path, name)
        print(fullname)
        write_log(fullname, logfile)