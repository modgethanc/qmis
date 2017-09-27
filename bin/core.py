#!/usr/bin/python

'''
QMIS inventory operations.

This module performs manipulations on the inventory dataset.

Vincent Zeng, Quartermaster
hvincent@modgethanc.com
'''

__author__="Vincent Zeng (hvincent@modgethanc.com)"

import os
import json
import time
import itertools

import util

## CONSTANTS
locations = ["eqo", "fac", "qmd", "ss", "dark", "dig", "hall", "class", "out"]
categories = ["camera body", "lens", "camera accessory", "tripod", "light meter", "lighting", "electronic", "tool", "book", "outfit", "timer", "darkroom accessory", "lighting accessory", "misc", "tripod head", "tripod legs"]
subcategories = ["35mm", "medium", "large", "digital", "enlarger", "none"]
statuses = ["circ", "surp", "sick", "scrap", "mia", "static", "deac", "staff", "unknown"]
defaults = ["make", "model", "name", "nick", "serial", "cmu", "provenance", "notes"]
lensdefaults = ["focal length", "aperture", "mount"]
bookdefaults = ["title", "author", "publisher", "isbn"]
nodefaults = [categories[3], categories[8], categories[9]]
multiples = [categories[0], categories[3], categories[4], categories[10]]
has_subcat = [categories[0], categories[1], categories[9]]

### basic data io

def new_entry(datafile, data):
    '''creates a new entry in dict j with dict data to dict made from
       filename.json'''

    validate(data)

    itemID = str(util.genID(5))
    while itemID in get_all_ids(datafile):
        # check for id collisions
        itemID = str(util.genID(5))

    newEntry = {itemID: data}

    return newEntry

### data manipulation

def validate(data):
    '''checks dict data for required elements'''

    if "date added" not in data:
        data.update({"date added":time.time()})
    if "status" not in data:
        data.update({"status":statuses[8]})
    if "subcat" not in data:
        data.update({"subcat":subcategories[5]})

    return data

def update_time(data):
    '''updates timestamp on a dict data'''

    if "last updated" not in data:
        data.update({"last updated":""})

    data["last updated"] = time.time()
    print("core: " + json.dumps(data))

    return data

def link_ids(datafile, ids):
    '''takes a list of ids from dict datafile and links them'''
    if len(ids) < 2:
        return

    for x in ids:
        for y in ids:
            if x != y:
                link_together(datafile, x, y)

    return ids

def link_together(datafile, source, target):
    '''adds target id to source link list'''

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
    # go through and remove all the blank fields and add unknowns

    item = get_by_id(datafile, itemID)[itemID]
    blanks = []

    for x in iter(item):
        if not item.get(x) or item.get(x) == "":
            blanks.append(x)

    for x in blanks:
        del item[x]

    if not item.get("status"):
        item.update({"status":statuses[8]})

    if not item.get("subcat"):
        item.update({"subcat":subcategories[5]})

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

## human-readable formatting

def display_name(item):
    # generates human-readable display name from raw item

    namegen = []
    nick = item.get("nick")
    name = item.get("name")
    make = item.get("make")
    model = item.get("model")
    focal = item.get("focal length")
    kit = item.get("kit")
    num = item.get("number")
    title = item.get("title")
    author = item.get("author")
    cat = item.get("cat")

    if nick:
        namegen.append(nick)
    elif name:
        namegen.append(name)
    elif make and model:
        namegen.append(make)
        namegen.append(model)
    elif model:
        namegen.append(model)
    elif make:
        namegen.append(make)
    elif kit:
        namegen.append(kit)
    elif title and author:
        namegen.append("\""+title+"\" "+author)

    if focal and not name:
        namegen.append(" "+focal)

    if num:
        namegen.append(" #"+num)

    if cat == categories[9]:
        namegen.append(" Kit")

    return " ".join(namegen)

def display_cat(item):
    # generates human-readable categories from raw item

    catgen = []
    cat = item.get("cat")
    subcat = item.get("subcat")

    if subcat == subcategories[4]:
        if cat == categories[0]:
            return "enlarger chassis"
        elif cat:
            return subcat + " " + cat
    else:
        if subcat and subcat != "none":
            catgen.append(subcat + " format ")
            if cat:
                catgen.append(cat)
        elif cat:
            catgen.append(cat)

    return " ".join(catgen)

def display_last_checked(item):
    # generates human-readable timestamp if it's a time, or show the value

    ts = item.get("last updated")

    if isinstance(ts, float):
        return time.strftime("%m/%d/%y %H:%M", time.localtime(ts))
    elif not ts:
        return ""
    else:
        return str(ts)

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
