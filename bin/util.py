#!/usr/bin/python

import random
import colorama

colorama.init()

rainbow = [
        colorama.Fore.RED,
        colorama.Fore.GREEN,
        colorama.Fore.YELLOW,
        colorama.Fore.BLUE,
        colorama.Fore.MAGENTA,
        colorama.Fore.WHITE,
        colorama.Fore.CYAN]

lastcolor = colorama.Fore.RESET

def genID(digits=5):
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
        color = random.choice(rainbow)

    lastcolor = color

    print(color, end="")

def resetcolor():
    print(colorama.Fore.RESET, end="")
