#!/usr/bin/python

import core

import json
import random
import fileinput
import os

datafile = {}
keys = []
files = []
working = ""
workingdir = ""

header = open("header.txt").read()
footer = "\nsee you later, space cowboy..."
divider = "\n\n\n\n\n"
invalid = "\nno idea what you mean; you gotta pick a number from the list!"
quickrel = "firing quick release!"

def start():
    print(header)
    print("")
    set_dir()
    print(main_menu())
    print(footer)

def end():
    print(divider)
    print("WRAPPING IT UP")
    print("!! always save your work! if you don't want to save your work, hit 'q' to burn it all away\n")

    return save_file()

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

## menu handlers

def print_menu(menu):
    i = 0
    for x in menu:
        print("\t[ ", end="")
        if i < 10:
            print(" ", end="")
        print(str(i)+" ] "+x)
        i += 1

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

    print("\nwhere do you want to save? (q to cancel) ", end="")
    save = ""
    choice = input()
    if choice =='q':
        return quickrel

    if int(choice) == i:
        print("enter new filename: ", end="")
        save = input()
        load_dir() # refresh file list!
    else:
        save = files[int(choice)]

    write(save)
    return "\nsaved to "+save 

def choose_file():
    global working
    print("\nLOADING FILE")

    print("i found these files: \n")
    print_menu(files)

    print("\npick one to load (q to cancel): ", end="")
    choice = input()
    if choice == "q":
        return quickrel

    working = int(choice)

    return (load(files[working]))

def view_detail():
    viewOptions = ["edit item", "stamp item", "link item", "unlink item", "change status", "change location"]

    print("single item ID: ", end="")
    itemID = input()
    print("")
    print(single_item(itemID))

    print("VIEWING DETAILS")
    print_menu(viewOptions)

    print("\ngonna do anything about it? (q to cancel) ", end="")

    choice = input()

    if choice == "0":
        return edit_item(core.get_by_id(datafile, itemID)[itemID])
    if choice == "1":
        return
    if choice == "2":
        return
    if choice == "3":
        return
    if choice == "4":
        return
    if choice == "5":
        return
    elif choice == "q":
        return quickrel 
    else:
        print(invalid)

    return view_detail()

def search_data():
    print("what's your search phrase? (i'm cap sensitive, sorry) ", end="")
    value = input()
    print("where do you want me to look for it? (still cap sensitive) ", end="")
    key = input()
    result = core.find_all(datafile, key, value)
    for x in result:
        print(pretty_data(core.get_by_id(datafile, x)))
    return ""

def count_data():
    print("COUNTING DATA")

    return "total: "+str(len(datafile))

def short_data():
    ids = core.get_all_ids(datafile)
    shortdata = {}
    for x in ids:
        raw = core.get_by_id(datafile, x)[x]
        item = {x:{"make":raw.get("make"), "model":raw.get("model")}}
        shortdata.update(item)

    return pretty_data(shortdata)

def pick_item():
    print("EDITING AN ITEM")
    print("\ngive me an ID: ", end="")
    itemID = input()

    return edit_item(core.get_by_id(datafile, itemID)[itemID])

def edit_item(raw):
    fields = []

    i = 0
    for x in iter(raw):
        print("\t[ ", end="")
        if i < 10:
            print(" ", end="")
        print(str(i)+" ] "+x+": "+str(raw.get(x)))
        i += 1
        fields.append(x)

    print("what do you want to edit? (q to cancel) ", end="")
    choice = input()

    if choice =='q':
        return quickrel

    key = fields[int(choice)]

    if key == "cat":
        value = core.categories[int(pick_cat())]
    elif key == "subcat":
        value = core.subcategories[int(pick_subcat())]
    else:
        print("\t"+key+": ", end="")
        value = input()

    raw.update({key:value})
    return edit_item(raw)

#def edit_handler():

def pick_subcat():
    print("valid subcategories:")
    print_menu(core.subcategories)
    print("\npick one: ", end="")
    return input()

def pick_cat():
    print("valid categories:")
    print_menu(core.categories)
    print("\npick one: ", end="")
    return input()

## menu views

def main_menu():
    menuOptions = ["manipulate current dataset", "load new dataset", "save current dataset", "quit"]

    print("")
    print("GETTING THINGS DONE")
    print("-------------------")

    print_menu(menuOptions)

    print("\ntell me your desires: ", end="")
    choice = input()

    if choice == "0":
        print(divider)
        print(data_menu())
    elif choice == "1":
        print(choose_file())
    elif choice == "2":
        print(save_file())
    elif choice == "3":
        print(divider)
        return end()
    elif choice == 'q':
        return quickrel
    else:
        print(invalid)

    return main_menu()

def data_menu():
    dataOptions = ["show raw data", "short view", "view detail", "count items", "search", "edit item", "back to main"]
    print("")
    print("DATA BROWSING")
    print("-------------")

    print_menu(dataOptions)

    print("\ntell me your desires (q to cancel): ", end="")
    choice = input()

    if choice == "0":
        print("\nCURRENT DATASET:\b")
        print(pretty_data(datafile))
    elif choice == "1":
        print(short_data())
    elif choice == "2":
        print(divider)
        print(view_detail())
    elif choice == "3":
        print(divider)
        print(count_data())
    elif choice == "4":
        print(divider)
        print(search_data())
    elif choice == "5":
        print(divider)
        print(pick_item())
    elif choice == "6":
        return divider
    elif choice == 'q':
        return quickrel
    else:
        print(invalid)

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
    ids = core.get_all_ids(datafile)
    return core.get_by_id(datafile, random.choice(ids))

def pretty_data(data):
    return json.dumps(data, sort_keys=True, indent=2, separators=(',',':'))

def single_item(item):
    return pretty_data(core.get_by_id(datafile, item))

## manipulation

def add_new(data):
    # add new data to local datafile

    datafile.update(core.new_entry(datafile, data))

    return k

def update_time(itemID):
    # update itemID with current timestamp

    item = core.update_time(core.get_by_id(datafile, itemID))
    datafile.update(item)

## DO THE THING

start()
