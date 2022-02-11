import sys
import os

import requests


# CONSTANTS
STATIC_MAPS_URL = 'https://static-maps.yandex.ru/1.x/'
GEOCODER_MAPS_URL = 'http://geocode-maps.yandex.ru/1.x/'

SIZE = [650, 450]
COORDS = [37.619015, 55.769393]
SPN = 0.001
MAP = 'map'
POINT = []
OBJECT_DATA = {}
ADD_POSTAL_CODE = False


# main funcs
j = lambda lst: ','.join([str(i) for i in lst])

def error(response, request):
    print("Ошибка выполнения запроса:")
    print(request)
    print("Http статус:", response.status_code, "(", response.reason, ")")

def get_coords(name):
    global OBJECT_DATA
    params = {
        'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
        'geocode': name,
        'format': 'json'
    }
    response = requests.get(GEOCODER_MAPS_URL, params=params)
    if response:
        try:
            json_response = response.json()
            OBJECT_DATA = json_response["response"]["GeoObjectCollection"]["featureMember"][0]
            return ','.join(OBJECT_DATA["GeoObject"]["Point"]["pos"].split())
        except IndexError as e:
            error(response, GEOCODER_MAPS_URL)
    else:
        error(response, GEOCODER_MAPS_URL)


# requests
def update_image():
    params = {
        "ll": j(COORDS),
        "size": j(SIZE),
        "spn": j([SPN] * 2),
        "l": MAP
    }
    if POINT:
        params.update({"pt": j(POINT) + ',pmgns'})
    response = requests.get(STATIC_MAPS_URL, params=params)
    if response:
        with open('data/map.png', "wb") as file:
            file.write(response.content)
    else:
        error(response, STATIC_MAPS_URL)

