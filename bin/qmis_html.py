#!/usr/bin/python

import os
import json
import time
import itertools

import util
import core

## CONSTANTS

coloredstatus = ["\"green\">in circulation", "\"blue\">surplus", "\"orange\">sick", "\"orange\">scrap bin","\"red\">mia", "\"black\">permanent", "\"red\">deaccessioned", "\"black\">staff/faculty use", "\"gray\">unknown"]

statuscolor = ["green", "blue", "orange", "orange", "red", "black", "red", "black", "gray"]

## helpers

def colored_status(item):
    # generates html-colored status

    status = item.get("status")

    if status:
        return "<font color="+coloredstatus[core.statuses.index(status)]+"</font>"

    else:
        return ""

def status_color(item):
    # returns color that status should be

    status = item.get("status")

    if status:
        return statuscolor[core.statuses.index(status)]
    else:
        return "black"

## html outputting

def html_one(datafile, itemID):
    unit = []

    item = core.get_by_id(datafile, itemID)[itemID]
    links = item.get("links")

    subclass = item.get("subcat")
    if subclass == "35mm":
        subclass = "thirtyfive"

    unit.append("<div class=\"item\"><div class=\""+subclass+"\"><a name=\""+itemID+"\"></a>")
    unit.append("\n\t<p><b>"+core.display_name(item)+"</b></p>") 

    unit.append("\n\t<p><small><i>"+core.display_cat(item)+"</i></small></p>")

    if links:
        linktext = "\n\t<p>bundled with: "
        if item.get("cat") == core.categories[9]:
            linktext = "\n\t<p>kit contents: "
        #unit.append("\n\t<p>bundled with: ")
        unit.append(linktext)
        for x in links:
            unit.append("<a href=\"#"+x+"\">"+core.display_name(core.get_by_id(datafile, x)[x])+"</a> ")
        unit.append("</p>")

    unit.append("\n\t<p align=\"right\"><small>"+colored_status(item)+"</small></p>")
    unit.append("\n\t<div class=\"meta\"><p><small>"+itemID+" "+str(item)+"</small></p></div>")

    unit.append("\n</div></div>\n")

    return "".join(unit)

def html_cat(datafile, category):
    # output everything of a certain category

    items = []
    ids = core.get_all_ids(datafile)
    subcats = dict(zip(core.subcategories, [[],[],[],[],[]]))
    other = []

    #print(category)
    for x in ids:
        item = core.get_by_id(datafile, x)[x]
        if item.get("cat") == category:
            subcat = item.get("subcat")
            if subcat and subcat != "none":
                subcats.get(subcat).append(x)
            else:
                other.append(x)

    for y in iter(subcats):
        for z in subcats.get(y):
            items.append(html_one(datafile, z))

    for y in other:
        items.append(html_one(datafile, y))

    return "".join(items)

def html_status(datafile, status):
    # output everything of a certain status

    items = []
    ids = core.get_all_ids(datafile)

    sorted(dictionary.items(), key=lambda x: x[1])

#### TESTING

def cats(datafile):
    outfile = open("www/testcats.html", "w+")
    outfile.write("<html><head>\n<title>QMIS OUTPUT TEST</title>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"></link>\n</head>\n<body>")
    outfile.write("<p>this file is automatically generated from QMIS. do not take it too seriously right now.</p>\n\n")
    outfile.write("<div class=\"nav\">\n")
    outfile.write("<p><i>last updated:<br>"+time.strftime("%d %b %Y, %H%M")+"</i></p>\n<ul>\n")

    outfile.write("<p>quick jumps:</p>\n") 
    for x in core.categories:
        outfile.write("<li><a href=\"#"+x+"\">"+x+"</a></li>\n")
    
    outfile.write("<p><b>color codes:</b></p>\n")
    outfile.write("<p style=\"background-color: lightyellow;\">35mm</p>")
    outfile.write("<p style=\"background-color: lightblue;\">digital</p>")
    outfile.write("<p style=\"background-color: lightpink;\">medium</p>")
    outfile.write("<p style=\"background-color: springgreen;\">large</p>")
    outfile.write("</ul></div>\n")
  
    for y in core.categories:
        outfile.write("<br clear=\"all\"><h3>"+y+"<a name=\""+y+"\"></a></h3>\n")
        outfile.write(html_cat(datafile, y))
   
    outfile.write("</body></html>")
    outfile.close()

def sortable(datafile):
    outfile = open("www/test_sort.html", "w+")

    outfile.write("<html><head>\n<title>QMIS OUTPUT TEST</title>\n<script src=\"sorttable.js\"></script>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" /></link>\n</head>\n<body>")
    outfile.write("<p>this file is automatically generated from QMIS. do not take it too seriously right now.</p>\n\n")
    outfile.write("<p><i>last updated:<br>"+time.strftime("%d %b %Y, %H%M")+"</i></p>\n")
    outfile.write("<div class=\"dataset\">\n<table class=\"sortable\">")
    outfile.write("<th>Name</th><th>Make</th><th>Model</th><th>Category</th><th>CMU ID</th><th>Links</th><th>Last Updated</th><th>ID</th>\n")

    for itemID in datafile:
        item = core.get_by_id(datafile, itemID)[itemID]
        outfile.write("<tr style=\"color:"+status_color(item)+"\"><td>")
        outfile.write(core.display_name(item)+"</td><td>")
        #outfile.write(str(item.get("name"))+"</td><td>")
        outfile.write(str(item.get("make"))+"</td><td>")
        outfile.write(str(item.get("model"))+"</td><td>")
        outfile.write(core.display_cat(item)+"</td><td>")
        #outfile.write(str(item.get("cat"))+"</td><td>")
        #outfile.write(str(item.get("subcat"))+"</td><td>")
        outfile.write(str(item.get("cmu"))+"</td><td>")

        links = item.get("links")
        if links:
            for ID in links:
                outfile.write("<a href=\"#"+ID+"\">"+core.display_name(core.get_by_id(datafile,ID)[ID])+"</a> ")
        else:
            outfile.write(" ")
        outfile.write("</td><td>")
        outfile.write(core.display_last_checked(item)+"</td><td>")
        #outfile.write(str(item.get("last updated"))+"</td><td>")
        outfile.write(str(itemID)+"<a name=\""+itemID+"\"></a></td>")
        outfile.write("</tr>\n")

    outfile.write("</table></body></html>")
    outfile.close()
