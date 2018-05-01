"""
Fait :
- calcule la distance entre deux lieux
- determine si un lieu est un pays, et dans ce cas retourne la capitale

A faire :
- traduire la liste des pays en francais
- calcule le nombre d'événements dans un meme lieu a la meme date
"""

from geopy import *
from geopy import distance
from geopy.geocoders import *
from math import radians, cos, sin, asin, sqrt

from countries import countries
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# print (countries[1])
geolocator = Nominatim()

#Scrap location data from ID
location = geolocator.geocode('Paris France')

#Scrap location data from ID
# print(location.address)
# print((location.latitude, location.longitude))

def determinePays(lieu):
    """
    Determine si un lieu donne est un pays \n
    Si c'est le cas, remplace le lieu par la capitale du pays
    """
    dataPays = next((item for item in countries if item["name"] == lieu), False)
    if(dataPays):
        return (dataPays['capital'])


print(determinePays('Lyon'))

def distanceCalculation(lieu1,lieu2):
    """
    Calcule distance entre deux lieux (lieu1 and lieu2) en km\n
    Passe par la methode geodesic
    """
    location1 = geolocator.geocode(lieu1)
    location2 = geolocator.geocode(lieu2)

    return(distance.distance((location1.latitude, location1.longitude),\
     (location2.latitude, location2.longitude)).km)



"""
LIMITE NOUVEAU CODE
A IGNORER
"""
#
# def haversine(lon1, lat1, lon2, lat2):
#     """
#     Calculate the great circle distance between two points
#     on the earth (specified in decimal degrees)
#     """
#     # convert decimal degrees to radians
#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
#     # haversine formula
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * asin(sqrt(a))
#     # Radius of earth in kilometers is 6371
#     km = 6371* c
#     return km
#
# tup1 = ('Breton', 1897, "EPFL")
# tup2 = ('Soupault', 1901, "Pantheon")
# tup3 = ('Ernst', 1901, "Berlin")
# tup4 = ('Picabia', 1925, "London")
# tup5 = ('Benayoun', 1925, "London")
#
# liste_raw = [tup1,tup2,tup3, tup4, tup5]
#
# index_name = 0
# index_year = 1
# index_location = 2
#
# dico_year = {}
# dico_location = {}
#
# # print'Avant'
# # print year
#
# def classe_annee(input_list, output_list):
#     for i in range (len(input_list)):
#         if input_list[i][index_year] not in output_list: #if l'annee n'est pas dans le dict, creer une entrer dans le dict
#             output_list.update({input_list[i][index_year]:1})
#         elif input_list[i][index_year] in output_list: #sinon, ajouter un index a l'annee correspondante
#             output_list.update({input_list[i][index_year]:year[input_list[i][index_year]]+1})
#
# classe_annee(liste_raw, year)
#
# # print'\nApres classement par annee'
# # print year
#
# def classe_lieu(input_list, output_list):
#     for i in range (len(input_list)):
#         #print input_list[i][index_location]
#         #print geolocator.geocode(input_list[i][index_location])
#         if input_list[i][index_location] not in output_list:
#             output_list.update({input_list[i][index_location]:1})
#         elif input_list[i][index_location] in output_list:
#             output_list.update({input_list[i][index_location]:output_list[input_list[i][index_location]]+1})
# classe_lieu(liste_raw, location)
#
#
# #print(geopy.distance.distance(newport_ri, cleveland_oh).miles)
#
#
#
# # print'\nApres classement par lieu'
# # print location
#
# # print year.keys()
# # print location.keys()
# # print location.keys()[2]
#
# location_list = []
# coordinates_list = []
# for i in range (len(location.keys())):
#     location_list.append(geolocator.geocode(location.keys()[i]))
#
# for j in range (len(location_list)):
#     coordinates_list.append([(location_list[j]).address, (location_list[j]).latitude,(location_list[j]).longitude])
#
# # print coordinates_list
# #
# print coordinates_list[1][0]
# print coordinates_list[2][0]
# crissier = geolocator.geocode('Crissier')
# epfl = geolocator.geocode('EPFL')
#
#
# print haversine(crissier.longitude, crissier.latitude, epfl.longitude, epfl.latitude)
