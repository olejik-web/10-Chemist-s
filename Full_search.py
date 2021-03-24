import sys
from pprint import pprint
from Need_Function import need_function, lonlat_distance
from io import BytesIO
import requests
from PIL import Image
toponym_to_find = input()
# object_width, object_height = int(input()), int(input())
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json",
    }
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
json_response = response.json()
# pprint(json_response)
object_width, object_height = need_function(json_response)
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([str(object_width), str(object_height)]),
    "l": "map",
    'pt': '{},{},pmwtm1'.format(toponym_longitude, toponym_lattitude)
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
global_object_width = object_width
global_object_height = object_height
distance = 0
name = ''
chemist_address = ''
work_time = ''
def find_chemist():
    chemists = []
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    address_ll = ",".join([toponym_longitude, toponym_lattitude])
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass    
    json_response = response.json()
    object_width, object_height = need_function(json_response)
    for inx, elem in enumerate(json_response["features"]):
        if inx < 10:
            chemists.append([elem["properties"]["CompanyMetaData"]["Hours"], 
                             [str(c) for c in elem['geometry']['coordinates']]])
    for elem in chemists:
        # print('Everyday' in elem[0]['Availabilities'][0].keys())
        if 'Everyday' in elem[0]['Availabilities'][0].keys():
            elem[0] = "{0},pmgnl50".format(','.join(elem[1]))
        elif not elem[0]['Availabilities'][0].keys():
            elem[0] = "{0},pmgrl50".format(','.join(elem[1]))
        else:
            elem[0] = "{0},pmbll50".format(','.join(elem[1]))
    map_params = {
        "ll": address_ll,
        "spn": ",".join(('0.05', '0.05')),
        "l": "map",
        "pt": '~'.join([elem[0] for elem in chemists])
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)  
    return response
Image.open(BytesIO(find_chemist().content)).show()