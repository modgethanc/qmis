#!/usr/bin/python

import core
import time

defaults = {"links":"", "loc":"", "manual":"", "name":"", "nick":"", "provenance":""}

def digital_bodies(filename):
    raw = open(filename)
    data = []
    i = 0;

    for x in raw:
        if i==0:
            i += 1
            continue

        i += 1
        y = x.rstrip().split(',')
        if not y[0]:
            continue

        #print(y)
        item = dict(zip(["make", "model", "serial", "number", "cmu","last updated", "notes"],y))
        #print(item)
        data.append(item)

    for x in data:
        x.update({"cat":core.categories[0],"subcat":core.subcategories[3],"date added": time.time()})
        x.update(defaults)

    return data

def generic(filename, order, cat, subcat):
    raw = open(filename)
    data = []
    i = 0;

    for x in raw:
        if i==0:
            i += 1
            continue

        i += 1
        y = x.rstrip().split(',')
        if not y[0]:
            continue

        #print(y)
        item = dict(zip(order, y))
        #print(item)
        data.append(item)

    for x in data:
        x.update({"cat":core.categories[cat],"subcat":core.subcategories[subcat],"date added": time.time()})
        x.update(defaults)
        print(x)

    return data
