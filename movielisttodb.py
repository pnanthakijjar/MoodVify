"""
    Script to put movies in a text file into database
"""

import sqlite3
import collections
import re
import time

from MovieScriptSearch import getScriptFromName as gsfn
from MovieScriptSearch import formatIList
from MovieScriptSearch import findMoviesOnIMSDB as fmoi

EMOJI_LIST = (("comedy", "funny", "joke", "laugh", "haha", "humor", "entertain", "dipster", "fat", "black dudes"),\
              ("romantic", "loving", "love", "charm", "passion", "charming", "boyfriend", "girlfriend"),\
              ("sad", "heartbroken", "miserable", "sorry", "sick", "grief", "grieving", "disconsolate"),\
              ("scary", "horror", "scare", "terror", "fight", "disgust", "hate", "terrorize", "fright", "frightening", "panic", "panicked", "devil", "monster", "alien", "predator", "aliens"),\
              ("family", "mother", "mom", "kids", "brother", "people", "children", "child", "boys", "boy", "girl", "girls", "vacation", "video games", "video game", "television", "t.v."),\
              ("food", "cooking", "delicious", "yum", "yummy", "cuisine", "meal", "diet", "nutrition", "foodstuff", "snack", "meal", "dinner", "dessert", "home"),\
              ("murder", "crime", "mystery", "mysterious", "criminal", "killer", "serial", "suspense", "tragic", "gun", "guns", "kills", "kill", "killing", "thrill", "thriller"),\
              ("action", "sports", "gun", "gunplay", "chase", "run", "fight", "fights", "cop", "police", "mob", "mobster", "crime", "criminal", "injury"),\
              ("drama", "life", "space", "emotion", "emotions", "emotional", "exciting", "sad", "melodrama", "cry", "crying", "melody", "fancy", "story", "feeling", "feelings", "entertaining"),\
              ("musical", "music", "sing", "singing", "instrument", "piano", "guitar", "guitars", "song", "instrumental", "acapella"))

def setup():
    """
        sets up file and cursor connections
    """
    moviefile = open("movies.list", 'r')
    
    conn = sqlite3.connect('movie.db')
    conn.text_factory = str
    c = conn.cursor()

    #c.execute("DROP TABLE IF EXISTS movies")
    #c.execute("CREATE TABLE movies (name text, year int)")

    conn.commit()
    conn.close()
    
    return moviefile

def parse_movies(moviefile):
    """
        Parses file "movies.list" and puts movie names into database,
        can only use imdb provided movies.list file
    """

    conn = sqlite3.connect('movie.db')
    conn.text_factory = str
    c = conn.cursor()

    for line in moviefile:
        if line[0].isalpha():
            index = line.find('(')

            if index != -1:
                title = line[0:index - 1]
                year = line[index+1:index+5]
                c.execute("INSERT INTO movies VALUES (?, ?)", (title, year))

    conn.commit()
    c.close()

    print "c"
    
def createCatDB():
    """
        Goes through movies, searches for scripts. If scripts are there,
        puts it into a new table showing different categories
    """

    conn = sqlite3.connect('movie.db')
    conn.text_factory = str
    c = conn.cursor()
    d = conn.cursor()
    
    c.execute("DROP TABLE IF EXISTS movieCats")
    c.execute("CREATE TABLE movieCats (name text, cat text)")

    movieList = formatIList(fmoi())
    for name in movieList:
        t1 = time.time()
        script = str(gsfn(name))
        script = script[5:-6]
        print name
        
        if script:
            
            cats = getCat(script)
            
            if not cats:
                continue
                        
            if ", The" in name:
                name = "The " + name[0:-6]
            elif ", A" in name:
                name = "A " + name[0:-3]

            for cat in cats:
                d.execute("INSERT INTO movieCats VALUES (?, ?)", \
                          (name, cat))
                conn.commit()
                print cat + " commited"

            
        x = .5 - (time.time() - t1)
        if x > 0:
            time.sleep(x) #sleep to be nice to servers

    conn.commit()
    conn.close()
    
def getCat(movieScript):
    """
        Gets categories of movie based on the script. Returns list of categories
        it falls under.
    """

    thresholdFreq = .001
    count = []
    
    for e in EMOJI_LIST:
        cnt = 0
        for word in re.findall('\w+', str(movieScript).lower()):
            if word in e:
                cnt += 1
        count.append(cnt)

    count.append(len(re.findall(r'\w+', str(movieScript))))

    if count[len(count) - 1] > 0:
        frequency = [ 1.0 * x / count[len(count) - 1] for x in count]
        frequency.pop()
    else:
        return None

    cList = []
    for i, f in enumerate(frequency):
        if f > thresholdFreq:
            cList.append(EMOJI_LIST[i][0])

    return cList

def movieCatList():
    """
        Returns list of movies for each category, in order.
    """

    conn = sqlite3.connect('movie.db')
    c = conn.cursor()

    catList = []
    for e in EMOJI_LIST:
        temp = []
        for row in c.execute("SELECT * FROM movieCats WHERE cat=?", (e[0],)):
            temp.append(row[0])
        catList.append(temp)

    return catList
        
if __name__ == "__main__":
    #m = setup()
    #parse_movies(m)
    #createCatDB()
    pass
