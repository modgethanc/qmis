#!/usr/bin/python

import core

datafile = {}

def load(filename):
    global datafile

    datafile = core.open_file(filename)
    return "loaded "+filename

def write(filename):
    core.update_file(filename, datafile)
    return "updated "+filename

def add_new(status, data):
    if not status in datafile:
        datafile.update({status:{}})

    k = datafile[status]
    k.update(core.new_entry(datafile, status, data))

    return k
