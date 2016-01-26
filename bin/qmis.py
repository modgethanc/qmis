#!/usr/bin/python

import core

import json
import random
import fileinput
import os
import time

datafile = {}
lastSearch = []
scratch = []
keys = []
files = []
working = ""
workingdir = ""
longView = True
auto = ""

header = open("header.txt").read()
footer = "\nsee you later, space cowboy..."
divider = "\n\n\n\n\n"
invalid = "\nno idea what you mean; you gotta pick a number from the list!"
quickrel = "firing quick release!"

def start():
    print(header)
    print("")
    set_dir()
    try:
        print(main_menu())
    except ValueError:
        print("!!VOMIT!!\nthat was unexpected i'm starting over")
        print(main_menu())
    except KeyboardInterrupt:
        print("?PANIC?")
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

        if not input_yn("default directory does not exist. create it?"):
            return set_dir()
    else:
        load_dir()

    return(workingdir)

def autosave():
    global auto
    auto = files[int(working)]+".ats"
    write(auto)
    print("autosaved to "+auto)

## menu handlers

def print_menu(menu):
    print("OPTIONS!")
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
    global lastSearch

    print("SEARCH FILTERS")
    print("--------------")

    search = {}
    search = basic_settings(search)

    print("other field? (i'm cap sensitive sorry. leave blank to cancel) ", end="")
    key = input()
    if key:
        print("what's your search phrase? (still cap sensitive, sorry) ", end="")
        value = input()

        search.update({key:value})

    print("search terms: "+str(search))
    lastSearch = core.multisearch(datafile, search)
    for x in lastSearch:
        print(pretty_data(core.get_by_id(datafile, x)))
    return "total found: "+str(len(lastSearch))

def count_data():
    return "total items: "+str(len(datafile))

def show_dataset(data):
    if longView:
        return pretty_data(data)
    else:
        return short_data(data)

def toggle_view():
    global longView

    print("\nTOGGLE VIEW")
    print("currently in ", end="")
    if longView:
        query = "full data view. toggle to short view?"
    else:
        query = "short data view. toggle to full view?"

    if input_yn(query):
        longView = not longView
        return "toggling view"
    else:
        return "not toggling view"

def short_data(data):
    ids = core.get_all_ids(data)
    shortdata = {}
    for x in ids:
        raw = core.get_by_id(datafile, x)[x]
        item = {x:{"make":raw.get("make"), "model":raw.get("model"), "name":raw.get("name"), "nick":raw.get("nick")}}
        shortdata.update(item)

    return pretty_data(shortdata)

def pick_item():
    print("give me an ID: (q to cancel) ", end="")
    ans = input()
    ids = core.get_all_ids(datafile)

    if ans in ids:
        return ans
    elif ans == "q":
        return quickrel
    else:
        print("sorry, i didn't find that in the current dataset.")
        return pick_item()

def bookmark(itemID):
    scratch.append(itemID)
    return "added to scratchpad"

def stamp_item(itemID):
    print("\nSTAMP ITEM")
    now = time.localtime

    if input_yn("today is "+time.strftime("%d %B %Y")+". stamp this item with today?"):
        links = get_links(itemID)
        for x in links:
            update_time(x)
        return "roger! stamped that sucker and everything attached to it"
    else:
        return "okay, not stamping a thing here"

def link_item(itemID):
    print("what do you want to link this to? ", end="")
    target = pick_item()
    links = [itemID, target]
    for x in links:
        item = core.get_by_id(datafile, x)
        check = item.get(x).get("links")
        for y in check:
            if y not in links:
                links.append(y)
    for x in links:
        print(single_item(x))

    if input_yn("are you suuuuure you want to link them?"):
        core.link_ids(datafile, links)
        print("link successful")
        return
    else:
        print("LINK ABORTED")
        return

def unlink_item(itemID):
    if len(get_links(itemID)) < 2:
        return("it's not even linked to anything. so ronery.")

    if input_yn("are you suuure you want to break this away from its friends?"):
        core.unlink(datafile, itemID)
        return "the operation was a success."
    else:
        return "UNLINK ABORTED"


def change_status(itemID):
    statuscode = int(pick_status())
    links = get_links(itemID)
    for x in links:
        raw = core.get_by_id(datafile, x)[x]
        raw.update({"status":core.statuses[statuscode]})
    return "status updated!"

def change_loc(itemID):
    loccode = int(pick_loc())
    links = get_links(itemID)
    for x in links:
        raw = core.get_by_id(datafile, x)[x]
        raw.update({"loc":core.locations[loccode]})
    return "location updated!"

def enter_data(name):
    print(name +": ", end="")
    data = {name:input()}
    return data

def item_adder():

    print("ADDING NEW ITEM")

    item = {}
    item = basic_settings(item)

    if item.get("cat") not in core.nodefaults:
        for x in core.defaults:
            item.update(enter_data(x))
    elif item.get("cat") == core.categories[1]:
        for x in core.lensdefaults:
            item.update(enter_data(x))
    elif item.get("cat") == core.categories[8]:
        for x in core.bookdefaults:
            item.update(enter_data(x))

    if core.is_multiple(item):
        item.update(enter_data("number"))

    item.update({"links":[]})
    print(pretty_data(item))

    if input_yn("add this?"):
        new = core.new_entry(datafile, item)
        datafile.update(new)
        print(short_data(new))
        return("sweet! new toys.")
    else:
        return("chucking all that work out the window")


## input handlers

def input_int():
    # returns an int (TODO)

    ans = input()

    if ans.isdigit():
        return int(ans)
    elif not ans:
        return False
    else:
        print("it's gotta be a number from the list, or blank: ", end="")
        return input_int()

def input_yn(query):
    # returns boolean True or False

    print(query+" [y/n] ", end="")
    ans = input()

    while ans not in ["y", "n"]:
        print("'y' or 'n' pls: ", end="")
        ans = input()

    if ans == "y":
        return True
    else:
        return False

def validate_index(target, ans):
    # checks if ans is a valid index into list target

    while ans >= len(target) or ans < 0:
        print("no it's gotta be from the list! ", end="")
        ans = input_int()

    return ans

def pick_subcat():
    print_menu(core.subcategories)
    print("\n\t(leave blank for none)")
    print("\nset subcategory: ", end="")
    ans = input_int()

    if ans:
        ans = validate_index(core.subcategories, ans)
    
    return ans

def pick_cat():
    print_menu(core.categories)
    print("\n\t(leave blank for none)")
    print("\nset category: ", end="")
    ans = input_int()

    if ans:
        ans = validate_index(core.categories, ans)
    
    return ans

def pick_loc():
    print_menu(core.locations)
    print("\n\t(leave blank for none)")
    print("\nset location: ", end="")
    ans = input_int()

    if ans:
        ans = validate_index(core.locations, ans)
    
    return ans

def pick_status():
    print_menu(core.statuses)
    print("\n\t(leave blank for none)")
    print("\nset status: ", end="")
    ans = input_int()

    if ans:
        ans = validate_index(core.statuses, ans)
    
    return ans

def basic_settings(item):
    # runs down basic shit for dict item

    status = pick_status()
    print(divider)
    cat = pick_cat()
    print(divider)
    if cat <= 2:
        print(divider)
        subcat = pick_subcat()
    else:
        subcat = ""
    print(divider)
    loc = pick_loc()

    if status:
        item.update({"status":core.statuses[status]})
    if cat:
    #if cat != len(core.categories) and cat >= 0:
        item.update({"cat":core.categories[cat]})
    if subcat:
        item.update({"subcat":core.subcategories[subcat]})
    if loc:
        item.update({"loc":core.locations[loc]})

    return item

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
    global scratch

    dataOptions = ["show dataset", "show scratchpad", "clear scratchpad","show last search", "toggle view", "view detail", "count items", "search", "edit item", "add item", "back to main"]
    print("")
    print("DATA BROWSING")
    print("-------------")

    print_menu(dataOptions)

    print("\ntell me your desires (q to cancel): ", end="")
    choice = input()

    if choice == "0":
        print(show_dataset(datafile))
    elif choice == "1":
        for x in scratch:
            print(pretty_data(core.get_by_id(datafile, x)))
    elif choice == "2":
        scratch = []
    elif choice == "3":
        for x in lastSearch:
            print(pretty_data(core.get_by_id(datafile, x)))
        print("total found: "+str(len(lastSearch)))
    elif choice == "4":
        print(toggle_view())
    elif choice == "5":
        print(divider)
        itemID = pick_item()
        if itemID == quickrel:
            print(quickrel)
        else:
            print(view_detail(itemID))
    elif choice == "6":
        print(divider)
        print(count_data())
    elif choice == "7":
        print(divider)
        print(search_data())
    elif choice == "8":
        print(divider)
        itemID = pick_item()
        if itemID == quickrel:
            print(quickrel)
        else:
            print(edit_item(itemID))
    elif choice == "9":
        print(item_adder())
    elif choice == "10":
        return divider
    elif choice == 'q':
        return quickrel
    else:
        print(invalid)

    return data_menu()

def view_detail(itemID):
    global longView

    viewOptions = ["edit details", "stamp item", "link item", "unlink item", "change status", "change location", "bookmark"]

    print(divider)
    if len(get_links(itemID)) > 1:
        for x in get_links(itemID):
            print(single_item(x))
    else:
        print(single_item(itemID))

    print("ITEM DEETS")
    print("----------")
    print_menu(viewOptions)
    if not longView:
        print("\n\t[  a ] (show full detail view)")

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
    elif choice == "6":
        print(bookmark(itemID))
    elif choice == "q":
        return quickrel
    elif choice == "a" and not longView:
        longView = True
        print("full deets")
        print(single_item(itemID))
        print("short deets")
        longView = False
    else:
        print(invalid)

    autosave()
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

    raw.update(edit_field(key))
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

def single_item(itemID):
    if longView:
        data = core.get_by_id(datafile, itemID)
    else:
        raw = core.get_by_id(datafile, itemID)[itemID]
        data = {itemID:{"make":raw.get("make"), "model":raw.get("model")}}
    return pretty_data(data)

def get_links(itemID):
    links = []
    links.extend(core.get_by_id(datafile, itemID).get(itemID).get("links"))
    links.append(itemID)
    return links

## manipulation

def update_time(itemID):
    # update itemID with current timestamp

    print("stamping "+itemID)
    item = {itemID:core.update_time(core.get_by_id(datafile, itemID).get(itemID))}
    datafile.update(item)

def edit_field(key):
    # edits individual field

    if key == "cat":
        value = core.categories[pick_cat()]
    elif key == "subcat":
        value = core.subcategories[pick_subcat()]
    elif key == "loc":
        value = core.locations[pick_loc()]
    elif key == "status":
        value = core.statuses[pick_status()]
    else:
        print("\t"+key+": ", end="")
        value = input()

    return {key:value}

## DO THE THING

start()
