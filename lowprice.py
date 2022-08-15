from parser import parsing, get_hotel_photo


def get_content(html):
    hotel_name = html['name']
    hotel_address = html['address']['streetAddress']
    distance = html['landmarks'][0]['distance']
    hotel_prise = html['ratePlan']['price']['current']

    text = 'Hotel name: {name}\nAddress: {address}\nDistance from center: {dist}\nPrise: {price}\n'.format(
        name=hotel_name, address=hotel_address, dist=distance, price=hotel_prise)

    return text


def low_price_parsing(city_name, number_of_hotels, number_of_photo, photo, command):
    info = list()
    photos_url = list()
    data = parsing(city_name, number_of_hotels, number_of_photo, photo,  command)

    for elem in data['data']['body']['searchResults']['results']:
        if photo:
            id_hotels = elem['id']
            photos_url.append(get_hotel_photo(id_hotels, number_of_photo))

        result = get_content(elem)
        info.append(result)
    print(photos_url)
    return info
