import asyncio
import json
import re
import time
import requests
import numpy as np
import pandas as pd
from datetime import timedelta, date
from io import StringIO
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from config import OPEN_WEATHER_API_KEY, USER_AGENT, SINOPTIK_URL, city_coordinates


class SinoptikWebScraper:
    def __init__(self, latitude, longitude):
        self.url = SINOPTIK_URL
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

        response = requests.get(geocode_url, params=params)
        try:
            if response.status_code == 200:
                data = response.json()

                uk_city = data[0]["local_names"]['uk'].strip().lower().replace(' ', '-')
                print(f"uk: <{uk_city}>")
                return uk_city

            else:
                raise Exception(f"bad request with status code {response.status_code}")

        except Exception as error:
            print(f"Geocoding API error! Response will be without Sinoptik.ua data: {error}")

    async def current_weather(self):
        async with ClientSession() as session:
            if not self.city_name:
                return None

            url = f"{self.url}/погода-{self.city_name}"
            headers = {
                'User-Agent': USER_AGENT}

            async with session.get(url, headers=headers) as response:
                try:
                    if response.status == 200:
                        data = await response.text()

                        self.soup = BeautifulSoup(data, "html.parser")

                        current_weather = {
                            "location": self.__get_current_location(),
                            "weather": self.__get_current_weather(),
                        }

                        self.write_to_json(current_weather, 'sin_cur')
                        return current_weather

                    else:
                        raise Exception(f"bad request with status code {response.status}")

                except Exception as error:
                    print(f"Sinoptik weather data fetching error: {error}")

    def __get_current_location(self):
        location = self.soup.find(class_="cityName cityNameShort")

        return {
            "city": location.find("h1").text.strip(),
            "region": location.find(class_="currentRegion").text.strip()
        }

    def __get_current_weather(self) -> dict:
        current_elements = self.soup.find_all(class_="cur")
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

    async def forecast(self, number_days: int):
        if not self.city_name:
            return None
        try:
            tasks = []
            for i in range(number_days):
                weather_date = (date.today() + timedelta(days=i)).strftime("%Y-%m-%d")
                tasks.append(asyncio.create_task(self.get_forecat_weather(weather_date)))

            tasks.append(asyncio.create_task(self.__get_main_page_forecast_data()))

            # get async results
            results = await asyncio.gather(*tasks)

            # get location and min/max temps
            main_page_data = results.pop()

            # add min/max temps to result
            for i in range(number_days):
                results[i]["temp"]["min"] = main_page_data["temp"]["min"][i]
                results[i]["temp"]["max"] = main_page_data["temp"]["max"][i]
                results[i]["condition"] = main_page_data["conditions"][i]

            forecast = {
                "location": main_page_data["location"],
                "weather_list": results
            }

            self.write_to_json(forecast, "sin_forecast")
            return forecast

        except Exception as error:
            print(f"Sinoptik forecast data fetching error: {error}")

    async def get_forecat_weather(self, weather_date: str) -> dict:
        async with ClientSession() as session:
            url = f"{self.url}/погода-{self.city_name}/{weather_date}"
            headers = {
                'User-Agent': USER_AGENT}

            async with session.get(url, headers=headers) as response:
                if response.status == 200:

                    html_source = await response.text()
                    data = pd.read_html(StringIO(html_source))[0]

                    weather = {
                        "date": weather_date,
                        "temp": {
                            "night": self.__strip_temp(data["ночь"][2]),
                            "morn": self.__strip_temp(data["утро"][2]),
                            "day": self.__strip_temp(data["день"][2]),
                            "eve": self.__strip_temp(data["вечер"][2]),
                        },
                        "feels_like": {
                            "night": self.__strip_temp(data["ночь"][3]),
                            "morn": self.__strip_temp(data["утро"][3]),
                            "day": self.__strip_temp(data["день"][3]),
                            "eve": self.__strip_temp(data["вечер"][3]),
                        },
                        "pressure": round(data.loc[4].astype(float).mean() * 1.333, 2),
                        "humidity": round(data.loc[5].astype(float).mean(), 2),
                        "wind_speed": round(data.loc[6].astype(float).mean(), 2),
                        "precip_prob": round(np.mean([int(precip) if precip != '-' else 0 for precip in data.loc[7]]))
                    }

                    return weather
                else:
                    raise Exception(f"bad request to {url} with status code {response}")

    async def __get_main_page_forecast_data(self):
        async with ClientSession() as session:
            url = f"{self.url}/погода-{self.city_name}"
            headers = {
                'User-Agent': USER_AGENT}

            async with session.get(url, headers=headers) as response:

                if response.status == 200:

                    html_source = await response.text()
                    self.soup = BeautifulSoup(html_source, "html.parser")

                    return {
                        "conditions": self.__get_conditions(),
                        "temp": {
                            'min': self.__get_temps("min"),
                            'max': self.__get_temps("max"),
                        },
                        "location": self.__get_locations()
                    }

                else:
                    raise Exception(f"bad request to {url} with status code {response}")

    def __get_conditions(self):
        tabs = self.soup.find("div", class_="tabs").find_all("div", class_="weatherIco")
        conditions = [tab.get("title") for tab in tabs]
        return conditions

    def __get_temps(self, min_or_max):
        divs = self.soup.find_all("div", class_=min_or_max)
        temps = [self.__strip_temp(div.find("span").text) for div in divs]
        return temps

    def __get_locations(self):
        location = self.soup.find(class_="cityName cityNameShort")

        return {
            "city": location.find("h1").text.strip(),
            "region": location.find(class_="currentRegion").text.strip()
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

    lat, lon = city_coordinates["Mur"]

    weather_handler = SinoptikWebScraper(lat, lon)

    task = asyncio.create_task((weather_handler.current_weather()))

    await task

    print(time.time() - start_time)


async def main_forecast():
    start_time = time.time()

    # weather_handler = SinoptikWebScraper(lat, lon)

    weather_handler = SinoptikWebScraper(40.1814, 44.5144)

    task = asyncio.create_task((weather_handler.forecast(7)))

    await task

    print(time.time() - start_time)


if __name__ == "__main__":
    # start_time = time.time()
    #
    # lat, lon = city_coordinates["Vinn"]
    #
    # # weather_handler = SinoptikWebScraper(lat, lon)
    #
    # weather_handler = SinoptikWebScraper(lat, lon)
    #
    # asyncio.run(weather_handler.forecast(1))
    #
    # print("Time: ",time.time() - start_time)

    asyncio.run(main_forecast())
    # ~0.7
