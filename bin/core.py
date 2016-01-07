#!/usr/bin/python

import os
import json
import time

import util

def filename(status):
    return "../data/"+status+".json"

def openFile(status):
    # opens status.json file and returns list (blank if no file)

    if not os.path.isfile(filename(status)):
        return []
    else:
        return json.load(open(filename(status)))

def updateFile(status, j):
    # overwrites status.json file with dict j

    datafile = open(filename(status), 'w')
    datafile.write(json.dumps(j, sort_keys=True, indent=2, separators=(',', ':')))

def newEntry(info, status="none"):
    # adds a new entry with dict info to array made from status.json

    newEntry = {str(util.genID(5)): info}

    j = openFile(status)
    j.update(newEntry)
    updateFile(status, j)

    return j

## testing shit

print(openFile("test2"))
print(len(openFile("test2")))
#print(newEntry({"name":"oliver","loc":"eqo"},"test2"))

info = { "loc": ["eqo", "fac", "qmd", "ss", "dark", "dig", "hall", "class", "out"],
        "last updated": time.time(),
        "cat":["camera body", "camera lens", "camera accessory", "tripod", "light meter", "camera accessory", "lighting", "electronic", "tool", "book", "outfit", "timer", "darkroom accessory", "lighting accessory", "misc"],
        "subcat":["35mm", "medium", "large", "digital", "enlarger"],
        "make":"manufacturer",
        "model":"specific mode",
        "name":"common name",
        "serial":"manufacturer serial",
        "cmu":"cmu non-capital id",
        "nick":"disambiguating nickname",
        "number":"disambiguating number",
        "date added":time.time(),
        "provenance":"when/where/how acquired",
        "notes": "known issues",
        "manual": "link to manual file or info page",
        "links": "list of ids this item is bundled with"}

sample = {"sample":info}

updateFile("sample", sample)
