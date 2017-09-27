#!/usr/bin/python

'''QMIS utilities

This module provides some helper shortcuts for QMIS.

Vincent Zeng, Quartermaster
hvincent@modgethanc.com'''

__author__ = "Vincent Zeng (hvincent@modgethanc.com)"

import random
import colorama
import os
import json

colorama.init()

textcolors = [ colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.WHITE, colorama.Fore.CYAN]

lastcolor = colorama.Fore.RESET

def genID(digits=5):
    '''Generates a numeric ID with given number of digits (default 5)'''

    id = ""
    x  = 0
    while x < digits:
        id += str(random.randint(0,9))
        x += 1

    return id

def setrandcolor():
    global lastcolor

    color = lastcolor
    while color == lastcolor:
        color = random.choice(textcolors)

    lastcolor = color

    print(color, end="")

def resetcolor():
    print(colorama.Fore.RESET, end="")

def attachrandcolor():
    global lastcolor

    color = lastcolor
    while color == lastcolor:
        color = random.choice(textcolors)

    lastcolor = color
    return color

def attachreset():
    return colorama.Style.RESET_ALL

def hilight(text):
    return colorama.Style.BRIGHT+text+colorama.Style.NORMAL

def open_file(filename):
    '''opens filename.json file and returns dict (blank if no file)'''

    if not os.path.isfile(filename):
        return {}
    else:
        return json.load(open(filename))

def update_file(filename, j):
    '''overwrites filename.json file with dict j'''

    datafile = open(filename, 'w')
    datafile.write(json.dumps(j, sort_keys=True, indent=2, separators=(',', ':')))


def pretty_data(data):
    dump = ""

    for x in data:
        dump += attachrandcolor()
        dump += "[ "+hilight(x)+" ]\n"+json.dumps(data[x], sort_keys=True, indent=2, separators=(',',':'))
        dump += "\n\n"

    dump += attachreset()

    return dump

def print_menu(menu):
    i = 0
    for x in menu:
        setrandcolor()
        print("\t[ ", end="")
        if i < 10:
            print(" ", end="")
        print(str(i)+" ] "+x)
        i += 1
        resetcolor()

def refresh(header, leftover=""):
    '''Refresh the display and reprint the header. If there's a leftover
    message, print that as well.'''

    os.system("clear")
    setrandcolor()
    print(header)
    resetcolor()

    if leftover:
        print("> " + leftover + "\n")

