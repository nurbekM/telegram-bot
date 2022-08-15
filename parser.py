import requests
import json
import re

url_id_city = "https://hotels4.p.rapidapi.com/locations/search"
url_hotel_list = "https://hotels4.p.rapidapi.com/properties/list"
url_hotel_photo = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"


HEADERS = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "2abd221e49mshab69e9bfe66ad93p10dc37jsn04d1239df2d8"
}


def get_html(url, params=dict[str:str]):
    response = requests.request("GET", url, headers=HEADERS, params=params)
    return response


def get_hotel_id(city):
    querystring_id_city = {"query": f"{city}", "locale": "en_US"}
    response = get_html(url=url_id_city, params=querystring_id_city)
    html = json_load(data=response)
    city_id = html['suggestions'][0]['entities'][0]['destinationId']

    return city_id


def get_hotel_list(city_id, number_of_hotels, command):
    querystring_hotel_list = {"destinationId": f"{city_id}", "pageNumber": "1", "pageSize": f"{number_of_hotels}",
                              "checkIn": "2022-05-30",
                              "checkOut": "2022-06-10", "adults1": "1", "sortOrder": f"{command}",
                              "locale": "en_US", "currency": "USD"}
    response = get_html(url=url_hotel_list, params=querystring_hotel_list)
    html = json_load(data=response)
    return html


def get_hotel_photo(id_hotels, number_of_photo):
    photos_url = list()
    querystring = {"id": f"{id_hotels}"}
    response = requests.request("GET", url_hotel_photo, headers=HEADERS, params=querystring)
    html = json_load(response)

    for images in html['hotelImages']:
        image = images['baseUrl']
        image = re.sub(r'[{size}]\w{4}\D', 'z', image)
        photos_url.append(image)
        if len(photos_url) == int(number_of_photo):
            print(photos_url)
            return photos_url


def json_load(data):
    data = json.loads(data.text)

    with open('test..json', 'w') as file:
        json.dump(data, file, indent=4)
    return data


def parsing(city_name, number_of_hotels, number_of_photo, photo,  command):
    city_id = get_hotel_id(city=city_name)

    html = get_hotel_list(city_id=city_id, number_of_hotels=number_of_hotels, command=command)

    return html



