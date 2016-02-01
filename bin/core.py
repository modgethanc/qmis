#!/usr/bin/python

import os
import json
import time
import itertools

import util

## CONSTANTS
locations = ["eqo", "fac", "qmd", "ss", "dark", "dig", "hall", "class", "out"]
categories = ["camera body", "camera lens", "camera accessory", "tripod", "light meter", "lighting", "electronic", "tool", "book", "outfit", "timer", "darkroom accessory", "lighting accessory", "misc"]
subcategories = ["35mm", "medium", "large", "digital", "enlarger"]
statuses = ["circ", "surp", "sick", "scrap", "mia", "static", "deac"]
defaults = ["make", "model", "name", "nick", "serial", "cmu", "provenance", "notes"]
lensdefaults = ["focal length", "aperture", "mount"]
bookdefaults = ["title", "author", "publisher", "isbn"]
nodefaults = [categories[3], categories[8], categories[9]]
multiples = [categories[0], categories[3], categories[4], categories[10]]
has_subcat = [categories[0], categories[1], categories[9]]

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
    if not links:
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

def clean_all(datafile):
    # clean blanks from every entry

    ids = get_all_ids(datafile)

    for x in ids:
        clean_item(datafile, x)

def clean_item(datafile, itemID):
    # go through and remove all the blank fields

    item = get_by_id(datafile, itemID)[itemID]
    blanks = []

    for x in iter(item):
        if not item.get(x) or item.get(x) == "":
            blanks.append(x)

    for x in blanks:
        del item[x]

    return item

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

def get_all_fields(datafile):
    # returns a list of all fields

    fields = []

    for x in datafile:
        source = datafile[x].keys()
        for x in source:
            if x not in fields:
                fields.append(x)

    return fields

def get_all_values(datafile, field):
    # returns a list of all values for a given field

    values = []
    for x in datafile:
        check = datafile[x].get(field)
        if check not in values:
            values.append(check)

    return values

def multisearch(datafile, searchdict):
    # returns a list of all ids that satisfy search terms in the searchdict

    ids = get_all_ids(datafile)
    matches = []
    fields = iter(searchdict)

    for x in ids:
        found = True
        item = get_by_id(datafile, x)[x]

        for y in iter(searchdict):
            if item.get(y) == searchdict.get(y):
                found = True
            else:
                found = False
                break

        if found:
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

## output formatting

def html_one(datafile, itemID):
    unit = []

    item = get_by_id(datafile, itemID)[itemID]
    nick = item.get("nick")
    name = item.get("name")
    make = item.get("make")
    model = item.get("model")
    cat = item.get("cat")

    unit.append("<div class=\"item\">\n\t<p><b>")

    if nick:
        unit.append(nick+"</b>")
        if name:
            unit.append(" <i>"+name+"</i>")
        unit.append("</p>\n")

        if make and model:
            unit.append("\n\t<p>"+make+" "+model+"</p>\n")
    else:
        if name:
            unit.append(name+"</b>")
        elif make and model:
            unit.append(make+" "+model+"</b> ")
            if cat == categories[1]:
                focal = item.get("focal length")
                if focal:
                    unit.append(focal)
        else:
            unit.append("</b>")

        unit.append("</p>")
        unit.append("\n\t<div class=\"meta\"><p><small>"+str(item)+"</small></p></div>")

    unit.append("\n</div>\n")

    return "".join(unit)



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
