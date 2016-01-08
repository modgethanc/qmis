#!/usr/bin/python

import os
import json
import time

import util

## CONSTANTS
locations = ["eqo", "fac", "qmd", "ss", "dark", "dig", "hall", "class", "out"]
categories = ["camera body", "camera lens", "camera accessory", "tripod", "light meter", "camera accessory", "lighting", "electronic", "tool", "book", "outfit", "timer", "darkroom accessory", "lighting accessory", "misc"]
subcategories = ["35mm", "medium", "large", "digital", "enlarger", "none"]

### basic data io

def file_parse(filename):
    return "../data/"+filename+".json"

def open_file(filename):
    # opens filename.json file and returns dict (blank if no file)

    if not os.path.isfile(filename):
        return {}
    else:
        return json.load(open(filename))

#    if not os.path.isfile(file_parse(filename)):
#        return {}
#    else:
#        return json.load(open(file_parse(filename)))

def update_file(filename, j):
    # overwrites filename.json file with dict j

    datafile = open(filename, 'w')
    #datafile = open(file_parse(filename), 'w')
    datafile.write(json.dumps(j, sort_keys=True, indent=2, separators=(',', ':')))

    #return j

def new_entry(datafile, status, data):
    # creates a new entry in dict j with dict data to dict made from filename.json

    #j = open_file(filename)

    #if not status in j:
    #    j.update({status:{}})
    #k = j[status]

    validate(data)

    itemID = str(util.genID(5))
    while itemID in get_all_ids(datafile):
        # check for id collisions
        itemID = str(util.genID(5))

    newEntry = {itemID: data}
    #k.update(newEntry)
    #print(j)
    #update_file(filename, j)

    #return j
    return newEntry

### data manipulation

def validate(data):
    # checks dict data for required elements

    if "date added" not in data:
        data.update({"date added":time.time()})

    return data

def update_time(data):
    # updates timestamp on a dict data
    if "last updated" not in data:
        data.update({"last updated":""})

    data["last updated"] = time.time()
    return data

### data retrieval

def get_all_status(datafile, status):
    # returns a dict of everything in dict datafile of status

    if status in datafile:
        return datafile[status]
    else:
        return {}

def get_all_statuses(datafile):
    # returns a list of all statuses in dict datafile

    return iter(datafile)

def get_all_ids(datafile, status=""):
    # returns a list of all ids by status in filename.json

    ids = []

    if status:
        for x in iter(get_all_status(datafile, status)):
                ids.append(x)
    else:
        for x in get_all_statuses(datafile):
            for y in iter(get_all_status(datafile, x)):
                ids.append(y)

    return ids

def status_of_id(datafile, dataID):
    status = ""
    for x in get_all_statuses(datafile):
        if dataID in get_all_ids(datafile, x):
            return x

    return status

def get_by_id(datafile, dataID):
    # return a dict of named dataID in dict datafile
    item = {}
    ids = get_all_ids(datafile)

    if dataID in ids:
        item = {dataID:datafile[status_of_id(datafile, dataID)][dataID]}

    return item

def find_all(datafile, key, value):
    # return a list of all ids that match the value of key in dict datafile

    ids = get_all_ids(datafile)
    matches = []

    for x in ids:
        item = get_by_id(datafile, x)
        if item[x].get(key) == value:
            matches.append(x)

    return matches




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