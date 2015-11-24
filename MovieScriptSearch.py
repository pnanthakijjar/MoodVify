"""
    Finds the movie script of each movie in the db, and later will search them so
    we can categorize them
"""

import requests
import time
import html5lib
import sqlite3
import string

from bs4 import BeautifulSoup as bs
from numba import jit

def getScriptFromName(name):
    """
        Gets the movie script for each name
    """
    aBool = False
    theBool = False

    name1 = ""

    name = name.replace(' ', '-')

    url1 = "http://www.imsdb.com/scripts/{}.html".format(name)

    snf = "Script not found"

    try:
        text = requests.get(url1).text
    except:
        text = requests.get(url1).text
        
    #text2 = requests.get(url2).text

    #try to get correct text from url
    if snf in text:
        return None


    soup = bs(text, "html5lib")

    try:
        script = soup.findAll('pre')[0]
    except:
        return None

        
    #extract bold tags until none left
    try:
        while script.b.extract():
            pass
    except:
        pass



    return script

def findMoviesOnIMSDB():
    """
        finds what movies are on IMSDB so we can scrape their scripts.
        Returns list of unformatted .html links
    """

    url = "http://www.imsdb.com/alphabetical/{}"

    #get html in format '/Movie Scripts/{} Script.html' into htmlList
    htmlList = []
    for l in "0" + string.ascii_lowercase:
        url1 = url.format(l)
        text = requests.get(url1).text
        soup = bs(text, "html5lib")
        t1 = time.time()
        
        while True:
            try:
                p = soup.p.extract()
            except:
                break

            htmlList.append(str(p.find('a').get('href')))

        x = .5 - (time.time() - t1)
        if x > 0:
            time.sleep(x) #sleep to be nice to servers

    return htmlList

def formatIList(iList):
    """
        Formats list returned from findMoviesOnIMSDB, returns list of
        same length.
    """

    newList = []
    for html in iList:
        
        if html[-12] == ' ':
            name = html[15:-12]
        else:
            name = html[15:-11]

            
        newList.append(name)

    return newList

if __name__ == "__main__":
    l = formatIList(findMoviesOnIMSDB())
