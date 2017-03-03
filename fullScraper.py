# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:46:48 2016

@author: Levi
"""

import sys
import cleanAndVerify
import json
import time
import requests
from bs4 import BeautifulSoup as bs4

with open("C:\\Users\\Levi\\Desktop\\Craigslist\\new\\cleanAndVerify\\allMakes.txt") as f:
    edmundDict = json.load(f)

makeList = [make['name'] for make in edmundDict['makes']]

locations = ['minneapolis', 'bismarck', 'billings', 'boise', 'portland', 'seattle']



for l, location in enumerate(locations):
    IDs = []
    cars = {}
    
    for make in makeList:
        searchURL = "http://" + location + ".craigslist.org/search/cto?s="
        results = 0

        while results < 2500:
            response = requests.get(searchURL + str(results) + "&query=" + make)
            results += 100
            html = bs4(response.text, "html.parser")
            fields = html('a')
            
            for field in fields:
                start = str(field).find("href=\"")
                end = str(field).find(".html")
                if start != -1 and end != -1:
                    IDs.append(((str(field)[start+6:end]), location))
            time.sleep(2)
    print(location + " " + str(l))

    IDs = list(set(IDs))
    print(len(IDs))
    for i, ID in enumerate(IDs):
        URL = "https://" + ID[1] + ".craigslist.org" + ID[0] + ".html"
        response = requests.get(URL)
        html = bs4(response.text, "html.parser")
        
        if ID not in cars:
            cars[ID] = cleanAndVerify.getInfo(html)
        
        if i%10 == 0:
            time.sleep(15)
            print(i)
 
    with open("C:\\Users\\Levi\\Desktop\\Craigslist\\test case\\" + location + "keyData.csv", "w") as keyFile:
        with open("C:\\Users\\Levi\\Desktop\\Craigslist\\test case\\" + location + "textData.txt", "w") as textFile:
            for key in cars:
                car = cars[key]
                keyFile.write(str(key[0]) + "," + str(key[1]) + "," + str(car[0]) + "," + str(car[1]) + "," + str(car[2]) + "," + str(car[3]) + "," + str(car[4]) + "," + str(car[5]) + "," + str(car[6]) + "," + str(car[7]) + "\n")
                textFile.write(str(key[0]) + "|" + str(key[1]) + "|" + str(car[8]) + "|" + str(str(car[9]).replace("|", "").encode(sys.stdout.encoding, errors='replace')) + "|" + str(str(car[10]).replace("|", "").encode(sys.stdout.encoding, errors='replace')) + "\n")


