#!/usr/bin/python

import random

def genID(digits=5):
    id = ""
    x  = 0
    while x < digits:
        id += str(random.randint(0,9))
        x += 1

    return id
