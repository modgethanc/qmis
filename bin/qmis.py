#!/usr/bin/python

import core

import json
import random
import fileinput
import os

datafile = {}
keys = []
header = open("header.txt").read()
footer = "\nsee you later, space cowboy..."
files = []
working = "" 
workingdir = ""


#for x in fileinput.input():
#    files.append(fileinput.filename())
#    fileinput.nextfile()


def start():
    print(header)
    print("")
    set_dir()
    print(main_menu())
    print(footer)

## menus

def end():
    print("")
    print("WRAPPING IT UP")
    print("!! always save your work! if you don't want to save your work, hit ctrl-c\n")

    save_file()

def set_dir():
    global workingdir

    print("set working directory: ", end="")
    workingdir = input()

    if not os.path.isdir(workingdir):
        print("default directory does not exist. create it? [y/n] ", end="")
        if input() == "n":
            return set_dir()
    else:
        load_dir()

    return(workingdir)

def save_file():
    print("SAVING FILE")
    print("current file list:")
    i = 0
    for x in files:
        print("\t[ "+str(i)+" ] "+x, end="")
        if i == working:
            print(" (loaded)")
        else:
            print("")
        i += 1
    print("\t[ "+str(i)+" ] (other)")

    print("\nwhere do you want to save? ", end="")
    save = ""
    choice = int(input())
    if choice == i:
        print("enter new filename: ", end="")
        save = input()
        load_dir() # refresh file list!
    else:
        save = files[choice]
    
    write(save)
    return "\nsaved to "+save

def choose_file():
    global working
    print("LOADING FILE")

    print("i found these files: \n")
    i = 0
    for x in files:
        print("\t[ "+str(i)+" ] "+x)
        i += 1

    print("\npick one to load: ", end="")
    working = int(input())

    return (load(files[working]))

def main_menu():
    menuOptions = ["browse current dataset", "load new dataset", "save current dataset", "quit"]

    print("")
    print("GETTING THINGS DONE")
    print("-------------------")

    i = 0
    for x in menuOptions:
        print("\t[ "+str(i)+" ] "+x)
        i += 1

    print("\ntell me your desires: ", end="")
    choice = input()

    if choice == "0":
        print("\n\n\n\n\n")
        print(data_menu())
    elif choice == "1":
        print("\n\n\n\n\n")
        print(choose_file())
    elif choice == "2":
        print("\n\n\n\n\n")
        print(save_file())
    elif choice == "3":
        print("\n\n\n\n\n")
        return end()
    elif choice == 'q':
        return "FIRING QUICK RELEASE"
    else:
        print("\nno idea what you mean; you gotta pick a number from the list!")
    
    return main_menu()

def data_menu():
    dataOptions = ["show raw data", "count items", "search", "back to main"]
    print("")
    print("DATA BROWSING")
    print("-------------")

    i = 0
    for x in dataOptions:
        print("\t[ "+str(i)+" ] "+x)
        i += 1

    print("\ntell me your desires: ", end="")
    choice = input()
    
    if choice == "0":
        print("\n\n\n\n\n")
        print("CURRENT DATASET:\b")
        print(pretty_data(datafile))
    elif choice == "1":
        print("\n\n\n\n\n")
        print(count_data())
    elif choice == "2":
        print("\n\n\n\n\n")
        print(search_data())
    elif choice == "3":
        return "\n\n\n\n\n"
    else:
        print("\nno idea what you mean; you gotta pick a number from the list!")

    return data_menu()

## setup

def load_dir():
    global files
    files.clear()

    for x in os.listdir(workingdir):
        if os.path.isfile(os.path.join(workingdir, x)):
            files.append(x)

def load(filename):
    global datafile

    datafile = core.open_file(os.path.join(workingdir,filename))
    return "loaded "+filename

def write(filename):
    core.update_file(os.path.join(workingdir, filename), datafile)
    return "updated "+filename

## retrieval

def random_item():
    # return a random item

    ids = core.get_all_ids(datafile)
    return core.get_by_id(datafile, random.choice(ids))

def pretty_data(data):
    return json.dumps(data, sort_keys=True, indent=2, separators=(',',':'))

def count_data():
    print("COUNTING DATA")

    statuses = core.get_all_statuses(datafile)
    total = 0
    for x in statuses:
        count = len(core.get_all_status(datafile, x))
        print(x+": "+str(count))
        total += count

    return "total: "+str(total)

def search_data():
    print("what's your search phrase? (i'm cap sensitive, sorry) ", end="")
    value = input()
    print("where do you want me to look for it? (still cap sensitive) ", end="")
    key = input()
    result = core.find_all(datafile, key, value)
    for x in result:
        print(pretty_data(core.get_by_id(datafile, x)))
    return ""

## manipulation

def add_new(status, data):
    if not status in datafile:
        datafile.update({status:{}})

    k = datafile[status]
    k.update(core.new_entry(datafile, status, data))

    return k

def update_time(itemID):
    # returns new dict of itemID with current timestamp

    item = core.update_time(core.get_by_id(datafile, itemID))
    datafile[core.status_of_id(datafile, itemID)].update(item)

## DO THE THING

start()
