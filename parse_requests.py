import sys

import requests


STATIC_MAPS_URL = 'https://static-maps.yandex.ru/1.x/'
SIZE = 400


j = lambda lst: ','.join([str(i) for i in lst])


def error(response, request):
    print("Ошибка выполнения запроса:")
    print(request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)


def get_coords(name):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={name}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        return ','.join(json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split())
    else:
        error(response, geocoder_request)


def update_image(ll, spn='0.002', l='map'):
    params = {
        "ll": j(ll),
        "size": j([SIZE] * 2),
        "spn": j([spn] * 2),
        "l": l
    }
    print(params)
    response = requests.get(STATIC_MAPS_URL, params=params)
    if response:
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
    else:
        error(response, STATIC_MAPS_URL)

