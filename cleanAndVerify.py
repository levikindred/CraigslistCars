# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:07:08 2017

@author: Levi
"""

import json
import re

with open("C:\\Users\\Levi\\Desktop\\Craigslist\\new\\cleanAndVerify\\allMakes.txt") as f:
    edmundDict = json.load(f)

makesDict = {make['name']:make['name'] for make in edmundDict['makes']}

modelsDict = {make['name']:{model['name']:model['name'] for model in make['models']} for make in edmundDict['makes']}

with open("C:\\Users\\Levi\\Desktop\\Craigslist\\new\\cleanAndVerify\\altMakes.txt") as f:
    for line in f:
        line = line.replace('\n', '').split(',')
        makesDict[line[1]] = line[0]
        
with open("C:\\Users\\Levi\\Desktop\\Craigslist\\new\\cleanAndVerify\\altModels.txt") as f:
    for line in f:
        line = line.replace('\n', '').split(',')
        modelsDict[line[0]][line[2]] = line[1]

def getInfo(html):
    try:
        heading = html.find("title").contents[0]
    except:
        heading = ""
    try:
        body = "".join(list(map(str, (html.find('section', id = "postingbody").contents[2:])))).replace("<br>", "").replace("</br>", "").replace("\n", " ")
    except:
        body = ""
    try:
        date = str(html.find("time", class_ = "timeago"))[32:56]
    except:
        date = None
    fields = html('p', class_ = 'attrgroup')
    try:
        info = fields[0].find('b').contents[0]
    except:
        info = ""

    make = None
    model = None
    
    for key in makesDict:
        if (info.lower().find(key.lower()) != -1):
            make = makesDict[key]
            break
    if (make == None):
        for key in makesDict:
            if (heading.lower().find(key.lower()) != -1):
                make = makesDict[key]
                break
    if (make == None):
        for key in makesDict:
            if (body.lower().find(key.lower()) != -1):
                make = makesDict[key]
                break

    if (make != None):
        for key in modelsDict[make]:
            if (info.lower().find(" " + key.lower()) != -1):
                model = modelsDict[make][key]
                break
        if (model == None):
            for key in modelsDict[make]:
                if (heading.lower().find(" " + key.lower()) != -1):
                    model = modelsDict[make][key]
                    break
        if (model == None):
            for key in modelsDict[make]:
                if (body.lower().find(" " + key.lower()) != -1):
                    model = modelsDict[make][key]
                    break
    

    try:
        year = info[0:4]
    except:
        year = None
    
    try:
        price = html.find('span', 'price').contents[0][1:]
    except:
        price = None
    
    try:
        fields = str(fields[1]).replace("\n", "")
    except:
        fields = ""

    try:
        odometer = re.match(".*odometer: <b>([0-9]+)", fields).group(1)
    except:
        odometer = None
    try:
        cylinders = re.match(".*cylinders: <b>([0-9]+)", fields).group(1)
    except:
        cylinders = None
    try:
        title = re.match(".*title status: <b>([^<]+)", fields).group(1)
    except:
        title = None
    try:
        trans = re.match(".*transmission: <b>([^<]+)", fields).group(1)
    except:
        trans = None
    
    
    if price == None:
        try:
            price = re.search("$ *([0-9,]+)", (heading.lower() + body.lower())).group(1).replace(",", "")
        except:
            price = None
    
    if odometer == None:
        try:
            odometer = re.search("([0-9]+,*[0-9]+) (?=mile)", (heading.lower() + body.lower())).group(1).replace(",", "")
        except:
            odometer = None
    if odometer == None:
        try:
            odometer = re.search("([0-9,]+[x,]+) (?=mile)", (heading.lower() + body.lower())).group(1).replace(",", "")
            odometer += "0" * odometer.count("x")
            odometer = odometer.replace("x", "")
        except:
            odometer = None
    if odometer == None:
        try:
            odometer = re.search("([0-9]+)k", (heading.lower() + body.lower())).group(1) + "000"
        except:
            odometer = None
    
    try:
        int(year)
    except:
        try:
            temp = int(re.search("([0-9]+)", year).group(1))
            if temp > 20:
                temp += 1900
            else:
                temp += 2000
            year = str(temp)
        except:
            year = None
    
    return [model, make, year, price, odometer, cylinders, title, trans, date, heading, body]