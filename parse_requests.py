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


# main funcs
j = lambda lst: ','.join([str(i) for i in lst])

def error(response, request):
    print("Ошибка выполнения запроса:")
    print(request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

def get_coords(name):
    params = {
        'apikey': "40d1649f-0493-4b70-98ba-98533de7710",
        'geocode': name,
        'format': 'json'
    }
    response = requests.get(GEOCODER_MAPS_URL, params=params)
    if response:
        json_response = response.json()
        return ','.join(json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split())
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
    response = requests.get(STATIC_MAPS_URL, params=params)
    print(SPN)
    if response:
        with open('data/map.png', "wb") as file:
            file.write(response.content)
    else:
        error(response, STATIC_MAPS_URL)

