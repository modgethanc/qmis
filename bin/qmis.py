#!/usr/bin/python

import core

import json
import random
import fileinput
import os
import time

datafile = {}
keys = []
files = []
working = ""
workingdir = ""
longView = True

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
    print("\t[ a ] (other)")

    print("\nwhere do you want to save? (q to cancel) ", end="")
    save = ""
    choice = input()
    if choice =='q':
        return quickrel

    if choice == "a":
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

def show_dataset():
    print("\nCURRENT DATASET:\b")
    if longView:
        return pretty_data(datafile)
    else:
        return short_data()

def toggle_view():
    global longView

    print("\nTOGGLE VIEW")
    print("currently in ", end="")
    if longView:
        print("full data view. toggle to short view? [y/n] ", end="")
    else:
        print("short data view. toggle to full view? [y/n] ", end="")

    choice = input()
    if choice == "y":
        longView = not longView
        return "toggling view"
    elif choice == "n":
        return "not toggling view"
    else:
        return toggle_view()

def short_data():
    ids = core.get_all_ids(datafile)
    shortdata = {}
    for x in ids:
        raw = core.get_by_id(datafile, x)[x]
        item = {x:{"make":raw.get("make"), "model":raw.get("model")}}
        shortdata.update(item)

    return pretty_data(shortdata)

def pick_item():
    print("\ngive me an ID: (q to cancel) ", end="")
    ans = input()
    ids = core.get_all_ids(datafile)

    if ans in ids:
        return ans
    elif ans == "q":
        return quickrel
    else:
        print("sorry, i didn't find that in the current dataset.")
        return pick_item()

def stamp_item(itemID):
    print("\nSTAMP ITEM")
    now = time.localtime
    print("today is "+time.strftime("%d %B %Y")+". stamp this item with today? [y/n] ", end="")

    choice = input()

    if choice == "y":
        update_time(itemID)
        return "roger! stamped that sucker"
    elif choice == "n":
        return "okay, not stamping a thing here"
    else:
        return stamp_item(itemID)

def link_item(itemID):
    return

def unlink_item(itemID):
    return

def change_status(itemID):
    raw = core.get_by_id(datafile, itemID)[itemID]
    raw.update({"status":core.status[int(pick_status())]})
    return

def change_loc(itemID):
    raw = core.get_by_id(datafile, itemID)[itemID]
    raw.update({"loc":core.locations[int(pick_loc())]})
    return "location updated!"

def pick_subcat():
    print_menu(core.subcategories)
    print("\nset subcategory:", end="")
    return input()

def pick_cat():
    print_menu(core.categories)
    print("\nset category:", end="")
    return input()

def pick_loc():
    print_menu(core.locations)
    print("\nset location: ", end="")
    return input()

def pick_status():
    print_menu(core.statuses)
    print("\nset status: ", end="")
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
    dataOptions = ["show dataset", "toggle view", "view detail", "count items", "search", "edit item", "back to main"]
    print("")
    print("DATA BROWSING")
    print("-------------")

    print_menu(dataOptions)

    print("\ntell me your desires (q to cancel): ", end="")
    choice = input()

    if choice == "0":
        print(show_dataset())
    elif choice == "1":
        print(toggle_view())
    elif choice == "2":
        print(divider)
        itemID = pick_item()
        if itemID == quickrel:
            print(quickrel)
        else:
            print(view_detail(itemID))
    elif choice == "3":
        print(divider)
        print(count_data())
    elif choice == "4":
        print(divider)
        print(search_data())
    elif choice == "5":
        print(divider)
        itemID = pick_item()
        if itemID == quickrel:
            print(quickrel)
        else:
            print(edit_item(itemID))
    elif choice == "6":
        return divider
    elif choice == 'q':
        return quickrel
    else:
        print(invalid)

    return data_menu()

def view_detail(itemID):
    viewOptions = ["edit details", "stamp item", "link item", "unlink item", "change status", "change location"]


    print(single_item(itemID))
    print("\nITEM DEETS")
    print_menu(viewOptions)

    print("\ngonna do anything about it? (q to cancel) ", end="")

    choice = input()

    if choice == "0":
        print(edit_item(itemID))
    elif choice == "1":
        print(stamp_item(itemID))
    elif choice == "2":
        print(link_item(itemID))
    elif choice == "3":
        print(unlink_item(itemID))
    elif choice == "4":
        print(change_status(itemID))
    elif choice == "5":
        print(change_loc(itemID))
    elif choice == "q":
        return quickrel 
    else:
        print(invalid)

    return view_detail(itemID)

def edit_item(itemID):
    raw = core.get_by_id(datafile, itemID)[itemID]
    fields = []
    
    print("")
    print(single_item(itemID))
    print("\nEDITING DEETS")
    i = 0
    for x in iter(raw):
        print("\t[ ", end="")
        if i < 10:
            print(" ", end="")
        print(str(i)+" ] "+x+": "+str(raw.get(x)))
        i += 1
        fields.append(x)

    print("\n\t[  a ] (add new field)")

    print("what do you want to edit? (q to cancel) ", end="")
    choice = input()

    if choice =='q':
        return quickrel

    if choice == "a":
        print("whatcha calling this new 'field'? ", end="")
        key = input()
    else:
        key = fields[int(choice)]

    if key == "cat":
        value = core.categories[int(pick_cat())]
    elif key == "subcat":
        value = core.subcategories[int(pick_subcat())]
    elif key == "loc":
        value = core.locations[int(pick_loc())]
    elif key == "status":
        value = core.statuses[int(pick_status())]
    else:
        print("\t"+key+": ", end="")
        value = input()

    raw.update({key:value})
    return edit_item(itemID)

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

    item = {itemID:core.update_time(core.get_by_id(datafile, itemID)[itemID])}
    datafile.update(item)

## DO THE THING

start()
