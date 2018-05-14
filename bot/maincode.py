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
import unicodedata
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
#from calais.base.client import Calais

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

    #=============String===============

    """check that every word starts with upperletter and max length of 20 chars"""
    def isName(string):
        if string.istitle():
            #result = api.analyze('"""' + string + '"""')
            #return 'entities' in result
            for chunk in ne_chunk(pos_tag(word_tokenize(string))):
                if hasattr(chunk, 'label'):
                    if chunk.label() == 'PERSON':
                        #print(' '.join(c[0] for c in chunk))
                        return True

        return False

    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


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

        if div[div.index("</a>") + 7] == '-' or div[div.index("</a>") + 4] == '.' or div[div.index("</a>") + 7] == ' ':
            return
        else:
            skipDate = div[div.index("<a")+ 2:]
            tagCityStart = skipDate[skipDate.index("<a"):]
            tagCity = tagCityStart[:tagCityStart.index("</a>")]
            city = tagCity[tagCity.index(">") + 1:]
            skipCity = tagCityStart[tagCityStart.index("</a>")+6:tagCityStart.index("</li>")]

            class MyHTMLParser(HTMLParser):
                data = []
                def handle_starttag(self, tag, attrs):
                    if tag == 'a':
                        for attr in attrs:
                            if str(attr[0]) == 'title':
                                if isName(attr[1]):
                                    self.data.append(attr[1])

            parser = MyHTMLParser()
            parser.feed(skipCity)
            if len(parser.data) != 0:
                #print(year, city, parser.data)
                return (year, city, parser.data)


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

    def repulsePoints(tuples):
        for i in range (len(tuples)):
            for j in range (len(tuples)):
                if (i != j and tuples[i][1] == tuples[j][1] and tuples[i][2] == tuples[j][2]):
                    tuples[j][1] = tuples[i][1] + 0.005
                    tuples[j][2] = tuples[i][2] + 0.005
        return tuples

    def finalNameCoordTuple(tuples):
        """
        Produces an array 'output' containing [Name, latitude, longitude]
        If location is a country, then it changes it to its capital
        """
        output = []
        for tuple in tuples:
            strNames = (tuple[2][0])
            coord = geolocator.geocode(capitalIfCountry(tuple[1]))
            if(len(tuple[2])==1):
                output.append([strNames, coord.latitude, coord.longitude])
            else:
                for j in range (1,len(tuple[2])):
                    strNames+=', ' +(tuple[2][j])
                output.append([strNames, coord.latitude, coord.longitude])
        return repulsePoints(output)

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

    def createJson(inputData, year):
        """
        Takes array [Name, lat, long] for each year
        Outputs in .json such that it can be plotted
        """
        indent = '    '
        indent2 = '      '
        maxLimit = len(inputData)
        with open(str(year)+'.json', 'w') as outfile:
            outfile.write('['+'\n')
            for i in range (maxLimit):
                if i == (maxLimit-1):
                        outfile.write(indent + '{'+'\n')
                        outfile.write(indent2 + ' "proprietes" : '+'['+'"'+remove_accents(str(inputData[i][0]))+'"'+ ','+ str(inputData[i][1])+ ','+ str(inputData[i][2])+']'+'\n')
                        outfile.write(indent + '}'+'\n')
                else:
                    outfile.write(indent + '{'+'\n')
                    outfile.write(indent2 + ' "proprietes" : '+'['+'"'+remove_accents(str(inputData[i][0]))+'"'+ ','+ str(inputData[i][1])+ ','+ str(inputData[i][2])+']'+'\n')
                    outfile.write(indent + '}'+','+'\n')

            outfile.write(']')
        outfile.close()

    def createCoreList():
        counter = 1
        divDate = getNthDiv(stringSoup, counter)
        yearCityNameList = []
        while divDate != None:
            element = getYearCityAndName(divDate)
            if element is not None:
                yearCityNameList.append(element)
            counter += 1
            divDate = getNthDiv(stringSoup, counter)

        return yearCityNameList

    #print(createCoreList())
    #print(finalNameCoordTuple(createCoreList()))
    createJson(finalNameCoordTuple(createCoreList()),year)

masterFunction(1883)
