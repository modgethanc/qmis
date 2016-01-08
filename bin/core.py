#!/usr/bin/python

import os
import json
import time

import util

## CONSTANTS
locations = ["eqo", "fac", "qmd", "ss", "dark", "dig", "hall", "class", "out"]
categories = ["camera body", "camera lens", "camera accessory", "tripod", "light meter", "camera accessory", "lighting", "electronic", "tool", "book", "outfit", "timer", "darkroom accessory", "lighting accessory", "misc"]
subcategories = ["35mm", "medium", "large", "digital", "enlarger", "none"]

def file_parse(filename):
    return "../data/"+filename+".json"

def open_file(filename):
    # opens filename.json file and returns dict (blank if no file)

    if not os.path.isfile(file_parse(filename)):
        return {}
    else:
        return json.load(open(file_parse(filename)))

def update_file(filename, j):
    # overwrites filename.json file with dict j

    datafile = open(file_parse(filename), 'w')
    datafile.write(json.dumps(j, sort_keys=True, indent=2, separators=(',', ':')))

    #return j

def new_entry(filename, status, info):
    # adds a new entry with dict info to dict made from filename.json


    j = open_file(filename)

    #if status in j:
    #    k = j[status]
    #else:
    #    k.update({status:""})

    #k = get_all_status(filename, status)
    if not status in j:
        j.update({status:{}})

    k = j[status]

    newEntry = {str(util.genID(5)): info}
    k.update(newEntry)
    print(j)
    #j.update(k)
    update_file(filename, j)

    return j

def get_all_status(filename, status):
    # returns a dict of everything in filename.json of status

    j = open_file(filename)

    if status in j:
        return j[status]
    else:
        return {}


## testing shit

sampleInfo = { "loc":locations,
        "last updated":time.time(),
        "cat":categories,
        "subcat":subcategories,
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

#fake = {"loc": "my butt"}
#sample = {"none":{"sample":sampleInfo}}

#update_file("sample", sample)
#print(open_file("sample"))
#print(update_file("sample", new_entry("sample", "none", fake)))
