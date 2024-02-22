import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
import io
import requests
from PIL import Image


class Gecode:
    def __init__(self, adress):
        adress =  adress
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": adress,
            "format": "json"}

        self.response = requests.get(geocoder_api_server, params=geocoder_params)

        if not self.response:
            # обработка ошибочной ситуации
            pass

        # Преобразуем ответ в json-объект
        self.json_response = self.response.json()
        # Получаем первый топоним из ответа геокодера.
        self.toponym = self.json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        self.toponym_coodrinates = self.toponym["Point"]["pos"]
        # Долгота и широта:
        self.toponym_longitude, self.toponym_lattitude = self.toponym_coodrinates.split(" ")
        delta = self.spn()
        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
             "spn": ",".join([str(delta[0]), str(delta[1])]),
            "l": "map",
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)

        print(response.url)



        image = Image.open(io.BytesIO(response.content))
        image.save("C:\Work\maps\image.png")

    def spn(self):
        coords_l = self.toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
        coords_r = self.toponym["boundedBy"]["Envelope"]["upperCorner"].split()
        delta = abs((float(coords_l[0]) - float(coords_r[0])) / 1.7)
        delta1 = abs((float(coords_l[1]) - float(coords_r[1])) / 1.7)
        return delta, delta1




        # Собираем параметры для запроса к StaticMapsAPI:
    def points(self, obj):
        self.object = obj
        self.search_api_server = "https://search-maps.yandex.ru/v1/"
        self.api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

        address_ll = f"{self.toponym_longitude},{self.toponym_lattitude}"

        search_params = {
                "apikey": self.api_key,
                "text": self.object,
                "lang": "ru_RU",
                "ll": address_ll,
                "type": "biz"
            }

        self.response1 = requests.get(self.search_api_server, params=search_params)
        if not self.response1:
                # ...
            pass

            self.json_response1 = self.response1.json()

            # Получаем первую найденную организацию.
            organizations = list(self.json_response1["features"][0:10])
            print(organizations)
            organization = organizations[0]
            points = []
            color = []
            for el in organizations:
                try:
                    print(el["properties"]["CompanyMetaData"]["Hours"]["Availabilities"][0])
                    start = el["properties"]["CompanyMetaData"]["Hours"]["Availabilities"][0]["Intervals"][0]["from"][
                            :2]
                    finish = el["properties"]["CompanyMetaData"]["Hours"]["Availabilities"][0]["Intervals"][0]["to"]
                    st = int(start)
                    fin = int(finish[:2])
                    color.append('pm2blm')
                except KeyError:
                    color.append('pm2dgm')
                except:
                    color.append('pm2grm')

                point1 = el["geometry"]["coordinates"]
                org_point = "{0},{1}".format(point1[0], point1[1])
                points.append(org_point)
            # Название организации.
            org_name = organization["properties"]["CompanyMetaData"]["name"]
            # Адрес организации.
            org_address = organization["properties"]["CompanyMetaData"]["address"]

            # Получаем координаты ответа.

            map_params = {
             #   "ll": ",".join([str(point1[0]), str(point1[1])]),
               # "spn": ",".join([str(delta[0]), str(delta[1])]),
                "l": "map",
                "pt": f"{self.toponym_longitude},{self.toponym_lattitude},pm2rdm~{points[0]},{color[0]}~{points[1]},{color[1]}~{points[2]},{color[2]}"
                      f"~{points[3]},{color[3]}~{points[4]},{color[4]}~{points[5]},{color[5]}~{points[6]},{color[6]}~{points[7]},{color[7]}"
                      f"~{points[8]},{color[8]}~{points[9]},{color[9]}"
            }

            map_api_server = "http://static-maps.yandex.ru/1.x/"
            # ... и выполняем запрос
            response = requests.get(map_api_server, params=map_params)

            print(response.url)


            image = Image.open(io.BytesIO(response.content))
            image.save("C:\Work\maps\image.png")

    def one_point(self,org):
        print(org)
        search_api_server = "https://search-maps.yandex.ru/v1/"
        org = org
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        address_ll = f"{self.toponym_longitude},{self.toponym_lattitude}"
        search_params = {
            "apikey": self.api_key,
            "text": "аптека",
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz"
        }

        response1 = requests.get(search_api_server, params=search_params)
        print(response1)
        if not response1:
            # ...
            pass
        json_response1 = response1.json()
        print(json_response1)
        # Получаем первый топоним из ответа геокодера.


        # Получаем первую найденную организацию.
        organization = json_response1["features"][1]
        # Название организации.
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        # Адрес организации.
        org_address = organization["properties"]["CompanyMetaData"]["address"]

        # Получаем координаты ответа.
        point1 = organization["geometry"]["coordinates"]
        print(point1)
        org_point = "{0},{1}".format(point1[0], point1[1])
        delta = "0.005"



        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "spn": ",".join([str(delta[0]), str(delta[1])]),
            #   "ll": ",".join([str(point1[0]), str(point1[1])]),
            # "spn": ",".join([str(delta[0]), str(delta[1])]),
            "l": "map",
            "pt": f"{self.toponym_longitude},{self.toponym_lattitude},pm2rdm"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)

        print(response.url)





        image = Image.open(io.BytesIO(response.content))
        image.save("C:\Work\maps\image.png")
