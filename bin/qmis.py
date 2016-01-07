#!/usr/bin/python

import os
import json

import util

def filename(status):
    return "../data/"+status+".json"

def openFile(status):
    # opens status.json file and returns dict (blank if no file)

    if not os.path.isfile(filename(status)):
        return {}
    else:
        return json.load(open(filename(status)))

def updateFile(status, j):
    datafile = open(filename(status), 'w')
    datafile.write(json.dumps(j))
    return j

def newEntry(status="none"):
    info = {"name": "ron", "loc": "out"}
    newEntry = {str(util.genID(5)): info}

    j = openFile(status)
    j.append(newEntry)

    return j

## testing shit

print(openFile("test2"))
print(newEntry("test2"))

updateFile("test2", newEntry("test2"))
