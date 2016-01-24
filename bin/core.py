#!/usr/bin/python

import os
import json
import time

import util

## CONSTANTS
locations = ["eqo", "fac", "qmd", "ss", "dark", "dig", "hall", "class", "out"]
categories = ["camera body", "camera lens", "camera accessory", "tripod", "light meter", "lighting", "electronic", "tool", "book", "outfit", "timer", "darkroom accessory", "lighting accessory", "misc"]
subcategories = ["35mm", "medium", "large", "digital", "enlarger"]
statuses = ["circ", "surp", "sick", "scrap", "mia", "deac"]
defaults = ["make", "model", "name", "nick", "serial", "cmu", "provenance", "notes"]
lensdefaults = ["focal length", "aperture", "mount"]
multiples = [categories[0], categories[3], categories[4], categories[10]]

### basic data io

def open_file(filename):
    # opens filename.json file and returns dict (blank if no file)

    if not os.path.isfile(filename):
        return {}
    else:
        return json.load(open(filename))

def update_file(filename, j):
    # overwrites filename.json file with dict j

    datafile = open(filename, 'w')
    datafile.write(json.dumps(j, sort_keys=True, indent=2, separators=(',', ':')))

    #return j

def new_entry(datafile, data):
    # creates a new entry in dict j with dict data to dict made from filename.json

    validate(data)

    itemID = str(util.genID(5))
    while itemID in get_all_ids(datafile):
        # check for id collisions
        itemID = str(util.genID(5))

    newEntry = {itemID: data}

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
    print("core: " + json.dumps(data))

    return data

def link_ids(datafile, ids):
    # takes a list of ids from dict datafile and links them
    if len(ids) < 2:
        return
    
    for x in ids:
        for y in ids:
            if x != y:
                link_together(datafile, x, y)

    return ids

def link_together(datafile, source, target):
    # adds target id to source link list

    item = get_by_id(datafile, source)[source]
    links = item.get("links")
    if links == '':
        links = []

    if target not in links:
        links.append(target)

    item.update({"links":links})

def unlink(datafile, target):
    # remove target id from everything it's linked to
    item = get_by_id(datafile, target)[target]
    links = item.get("links")
    
    for x in links:
        unlink_from(datafile, x, target)

    item.update({"links":[]})

def unlink_from(datafile, source, target):
    # removes target id from source

    item = get_by_id(datafile, source)[source]
    links = item.get("links")
    links.remove(target)

    item.update({"links":links})

### data retrieval

def get_all_ids(datafile):
    # returns a list of all ids in filename.json

    return iter(datafile)

def get_by_id(datafile, dataID):
    # return a dict of named dataID in dict datafile

    item = {}
    ids = get_all_ids(datafile)

    if dataID in ids:
        item = {dataID:datafile[dataID]}

    return item

def multisearch(datafile, searchdict):
    # returns a list of all ids that satisfy search terms in the searchdict

    ids = get_all_ids(datafile)
    matches = []
    fields = iter(searchdict)

    for x in ids:
        found = False
        item = get_by_id(datafile, x)[x]

        for y in iter(searchdict):
            #print(item)
            #print("searching for "+y+":"+searchdict.get(y))
            print(item.get(y))
            if item.get(y) == searchdict.get(y):
                found = True
            else:
                found = False
                break 

        if found:
            #print("FOUND "+x)
            matches.append(x)

    return matches

def find_all(datafile, key, value):
    # return a list of all ids that match the value of key in dict datafile

    ids = get_all_ids(datafile)
    matches = []

    for x in ids:
        item = get_by_id(datafile, x)[x]
        if item.get(key) == value:
            matches.append(x)

    return matches

def is_multiple(item):
    return item.get("cat") in multiples 

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
