import sys
from pprint import pprint
from io import BytesIO
import requests
import math


def need_function(json_response):
    try:        
        json_envelope = \
            json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']
        object_x1, object_y1 = [float(elem) for elem in json_envelope['lowerCorner'].split()]
        object_x2, object_y2 = [float(elem) for elem in json_envelope['upperCorner'].split()]
    except:
        json_envelope = \
            json_response['features'][0]['properties']['boundedBy']
        object_x1, object_y1 = [float(elem) for elem in json_envelope[0]]
        object_x2, object_y2 = [float(elem) for elem in json_envelope[1]]
    object_width = object_x2 - object_x1
    object_height = object_y2 - object_y1
    return (object_width, object_height)

def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance