import asyncio
import json
import re
import time
from io import StringIO
from aiohttp import ClientSession
import requests
from bs4 import BeautifulSoup
import pandas as pd

from config import OPEN_WEATHER_API_KEY, city_coordinates, USER_AGENT

BASE_URL = 'https://ua.sinoptik.ua'


class SinoptikWebScraper:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.city_name = self.__get_city_name()
        self.soup = None


    def __get_city_name(self):
        geocode_url = "http://api.openweathermap.org/geo/1.0/reverse"

        params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "appid": OPEN_WEATHER_API_KEY,
            "limit": 1
        }

        star = time.time()
        response = requests.get(geocode_url, params=params)

        # print("Request time: " + str(time.time() - star))
        if response.status_code == 200:
            data = response.json()
            print("Geocoded data: ", data)
            try:
                uk_city = data[0]["local_names"]['uk'].strip().lower()
                print(f"uk: <{uk_city}>")
                return uk_city
            except KeyError:
                print("Couldn't find city! Response will be without Sinoptik.ua data.")
                return None

        else:
            print("Geocoding API error happened!")

    async def current_weather(self):
        async with ClientSession() as session:
            if not self.city_name:
                return None

            url = f"{BASE_URL}/погода-{self.city_name}"
            headers = {
                'User-Agent': USER_AGENT}

            async with session.get(url, headers=headers) as response:

                data = await response.text()
                self.soup = BeautifulSoup(data, "html.parser")
                try:
                    current_weather = {
                        "location": self.__get_current_location(),
                        "weather": self.__get_current_weather(),
                    }

                    self.write_to_json(current_weather, 'sin_cur')
                    return current_weather

                except AttributeError:
                    print("Sinoptik Scraping error!")
                    return None

    def __get_current_location(self):
        location = self.soup.find(class_="cityName cityNameShort")

        return {
            "city": location.find("h1").text.strip(),
            "region": location.find(class_="currentRegion").text.strip()
        }

    def __get_current_weather(self) -> dict:
        current_elements = self.soup.find_all(class_="cur")

        # (current_elements)

        precip_prob = current_elements[7].text

        return {
            "time": current_elements[0].text.replace(' ', ''),
            "condition": current_elements[1].find('div').get("title"),
            "temp": int(self.__strip_temp(current_elements[2].text)),
            "feels_like": int(self.__strip_temp(current_elements[3].text)),
            "pressure": round(int(current_elements[4].text) * 1.333, 2),  # to hPa (millibars)
            "humidity": int(current_elements[5].text),
            "wind_speed": float(current_elements[6].text),
            "precip_prob": 0 if precip_prob == '-' else int(precip_prob)
        }

    @staticmethod
    def __strip_temp(temp_str: str):
        matches = re.findall(r'[-+]?\d+°', temp_str)
        return int(matches[0][:-1]) if matches else None

    @staticmethod
    def write_to_json(data, file_name):
        with open(f"data/{file_name}.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


async def main_cur():
    start_time = time.time()

    lat, lon = city_coordinates["Vinn"]

    # weather_handler = SinoptikWebScraper(lat, lon)

    weather_handler = SinoptikWebScraper(lat, lon)

    task = asyncio.create_task((weather_handler.current_weather()))

    await task


    print(time.time() - start_time)

if __name__ == "__main__":

    asyncio.run(main_cur())
    # ~0.7
