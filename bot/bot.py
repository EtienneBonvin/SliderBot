from urllib.request import urlopen
from bs4 import BeautifulSoup

# oldest year found : 1765
# isnumeric() pour détecter si la date est bien récupéree

response=urlopen("http://wikipast.epfl.ch/wikipast/index.php/1970")
page_source=response.read()
soup=BeautifulSoup(page_source,'html.parser')
stringSoup = str(soup)

def getNthDiv(stringSoup, n):
    divStart = stringSoup[stringSoup.index("mw-content-ltr") + len("mw-content-ltr"):]
    
    for i in range(n):
        try:
            nextIndex = divStart.index("<li")
        except ValueError:
            return None
        
        divStart = divStart[nextIndex + len("<li"):]
    
    return divStart

def getYearAndCity(div):
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
        return (year, city)

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
    
counter = 1
divDate = getNthDiv(stringSoup, counter)
yearCityList = []
while divDate != None:
    element = getYearAndCity(divDate)
    if element is not None:
        yearCityList.append(element)
    counter += 1
    divDate = getNthDiv(stringSoup, counter)
    
#printTuples(yearCityList)
printBigTuples(tuplesWithMultiplicity(yearCityList))