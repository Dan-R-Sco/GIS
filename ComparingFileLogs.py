# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 14:09:28 2018

@author: daniel.scott
"""

"""
Creation of the dictionaries
@author: daniel.scott
"""
filepath = r'Q:\08_EXINT\01_KM\02_Projects\Search tool\V04_FolderCat.txt'
cnt = 0 
with open(filepath) as fp:
    line = fp.readline()
    dictDiego = {}
    while line:
        #print("line {}: {}".format(cnt, line.strip()))
        line = fp.readline()
        k = cnt
        v = line
        dictDiego.update({k:v})
        cnt +=1
        
filepath = r'Q:\08_EXINT\01_KM\02_Projects\Search tool\ICV04Folderlog.txt'
cnt = 0 
with open(filepath) as fp:
    line = fp.readline()
    dictDan = {}
    while line:
        #print("line {}: {}".format(cnt, line.strip()))
        line = fp.readline()
        k = cnt
        v = line
        dictDan.update({k:v})
        cnt +=1
        
print "Length of dictDan: %d" % len (dictDan)
print "Length of dictDiego: %d" % len (dictDiego)


import re, os
def is_matched(expression):
    """
    Finds out how balanced an expression is.
    With a string containing only brackets.

    >>> is_matched('[]()()(((([])))')
    False
    >>> is_matched('[](){{{[]}}}')
    True
    """
    opening = tuple('({[')
    closing = tuple(')}]')
    mapping = dict(zip(opening, closing))
    queue = []

    for letter in expression:
        if letter in opening:
            queue.append(mapping[letter])
        elif letter in closing:
            if not queue or letter != queue.pop():
                return False
    return not queue

if __name__ == '__main__':
    import doctest
    doctest.testmod()

cleandictDiego = {}
for k, value in dictDiego.iteritems():
    filen = os.path.split(os.path.abspath(value))[1]
    if is_matched(filen) == False:
        pass
    else:
        cleandictDiego.update({k:value})

print "Length of files that dont have escape characters: %d" % len (cleandictDiego)

"""
Checking the values against each other -- currently bug if directories have escape characters. Need to move to before running the check

@author: daniel.scott


duplications = {}
unique = {}
cnt = 0
cnt2 = 0
for key, value in dictDan.iteritems():
    #print value
    filen = os.path.split(os.path.abspath(value))[1]
    for v in cleandictDiego.itervalues():
        if is_matched(filen) == True:
            try:
                if re.search(filen,v):
                    print "match made for duplication: " + filen
                    cnt += 1
                    key = cnt
                    duplications.update({key:filen})
                else:
                    pass
            except:
                print "unable to process: " + filen
                pass
        else: 
            print "Unable to compare as has escape value: " + filen
            continue
        
print "Length of duplications: %d" % len (cleandictDiego)
## if want can add
#for item in duplications.iteritems():
#write_log(item,log)
print "Finished!"
"""

