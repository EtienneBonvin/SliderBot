from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import io
import json
import time
from countries import countries
from geopy import *
from geopy.geocoders import *
from html.parser import HTMLParser
import spacy

# oldest year found : 1765
# isnumeric() pour détecter si la date est bien récupéree

def masterFunction(year):
    """
    Core function : creates a JSON file with [Name, lat, long]
    for any year (argument)
    """
    #==========Initialisation===========

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    response=urlopen("http://wikipast.epfl.ch/wikipast/index.php/"+str(year))
    page_source=response.read()
    soup=BeautifulSoup(page_source,'html.parser')
    stringSoup = str(soup)
    geolocator = Nominatim()
    nlp = spacy.load('fr')

    #=============Parsing===============

    def getNthDiv(stringSoup, n):
        divStart = stringSoup[stringSoup.index("mw-content-ltr") + len("mw-content-ltr"):]

        for i in range(n):
            try:
                nextIndex = divStart.index("<li")
            except ValueError:
                return None

            divStart = divStart[nextIndex + len("<li"):]

        return divStart

    def getYearCityAndName(div):
        tagDate = div[div.index("<a"):div.index("</a>")]
        date = tagDate[tagDate.index(">") + 1:]
        year = date.split(".")[0]

        if not year.isnumeric():
            return

        if div[div.index("</a>") + 7] == '-':
            return
        else:
            skipDate = div[div.index("<a")+ 2:]
            tagCityStart = skipDate[skipDate.index("<a"):]
            tagCity = tagCityStart[:tagCityStart.index("</a>")]
            city = tagCity[tagCity.index(">") + 1:]
            skipCity = tagCityStart[tagCityStart.index("</a>")+6:tagCityStart.index("</li>")]

            class MyHTMLParser(HTMLParser):
                def handle_starttag(self, tag, attrs):
                    if tag == 'a':
                        for attr in attrs:
                            if str(attr[0]) == 'title':
                                persons = [token for token in nlp(attr[1]) if token.ent_type_ == 'PERSON']
                                print('Sentence : ' + attr[1])
                                print('Tokens : '+ persons)

            parser = MyHTMLParser()
            parser.feed(skipCity)

            """
            tagDivStart = skipCity[skipCity.index("<a"):]
            tagDiv = tagDivStart[:tagDivStart.index("</a>")]
            divName = tagDiv[tagDiv.index(">") + 1:]
            print(divName)"""

            return (year, city)

    #===========Location===========

    def capitalIfCountry(location):
        """
        If location is a country, then it changes it to its capital
        """
        dataPays = next((item for item in countries if item["name"] == location), False)
        if(dataPays):
            return (dataPays['capital'])
        else:
            return location

    def finalNameCoordTuple(tuples):
        """
        Produces an array 'output' containing [Name, latitude, longitude]
        If location is a country, then it changes it to its capital
        """
        output = []
        for tuple in tuples:
            coord = geolocator.geocode(capitalIfCountry(tuple[1]))
            output.append(['None', coord.latitude, coord.longitude])
        return output

    #=============Print=============

    def printTuples(tuples):
        for tuple in tuples:
            print(tuple[0]+" : "+tuple[1])

    def tuplesWithMultiplicity(yearCityList):
        tuples = []
        for i in range(0, len(yearCityList)):
            compte = yearCityList.count(yearCityList[i])
            tuples.append((yearCityList[i], compte))

        return [list(item) for item in set(tuple(row) for row in tuples)]

    def printBigTuples(tuples):
        for tuple in tuples:
            print(tuple[0][0], tuple[0][1], tuple[1])

    def printFinalTuples(tuples):
        for tuple in tuples:
            print('Who : ' + tuple[0] + ' Where : ' + tuple[1] + ' ' + tuple[2])

    #===========JSON file===========

    def createJsonFile(tuples, year):
        """
        Creates a JSON file 'year.json' containing [Name, latitude, longitude] arrays
        """
        with open(str(year)+'.json', 'w') as outfile:
            json.dump(tuples, outfile, indent=4)

    def createCoreList():
        counter = 1
        divDate = getNthDiv(stringSoup, counter)
        yearCityList = []
        while divDate != None:
            element = getYearCityAndName(divDate)
            if element is not None:
                yearCityList.append(element)
            counter += 1
            divDate = getNthDiv(stringSoup, counter)

        return yearCityList

    createJsonFile(finalNameCoordTuple(createCoreList()), year)

masterFunction(1960)

#======Looping Test=======

# for yearIndex in range (1960,1970):
#     time.sleep(10)
#     print('Doing ' + str(yearIndex))
#     time.sleep(20)
#     masterFunction(yearIndex)
