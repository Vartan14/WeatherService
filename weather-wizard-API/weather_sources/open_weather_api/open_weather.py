import requests
import json
from bs4 import BeautifulSoup
from config import OPEN_WEATHER_API_KEY
from datetime import datetime, timedelta
import time
from aiohttp import ClientSession


class OpenWeatherAPI:
    def __init__(self, latitude, longitude):
        self.base_url = "https://api.openweathermap.org/data/2.5"

        self.params = {
            "lat": latitude,
            "lon": longitude,
            "appid": OPEN_WEATHER_API_KEY,
            "units": "metric"
        }

        self.api_data = None

    async def current_weather(self):
        async with ClientSession() as session:
            url = f"{self.base_url}/weather"

            async with session.get(url, params=self.params) as response:
                self.api_data = await response.json()

                try:
                    current_weather = {
                        "location": self.__get_current_location(),
                        "weather": self.__get_current_weather()
                    }

                    self.write_to_json(current_weather, "ow_cur")

                    return current_weather

                except KeyError:
                    print("OpenWeatherAPI data fetching error.")
                    return None



    def __get_current_weather(self):
        weather = {
            # weather time
            "time": str(datetime.fromtimestamp(self.api_data["dt"])),
            # weather description
            "condition": self.api_data['weather'][0]['main'],
            "desc": self.api_data['weather'][0]['description'],
            "icon_code": self.api_data['weather'][0]['icon'],

            # temperature in Celsius
            "temp": self.api_data['main']['temp'],
            "feels_like": self.api_data['main']['feels_like'],

            # "temp_min": self.api_data['main']['temp_min'],
            # "temp_max": self.api_data['main']['temp_max'],

            # other properties
            "pressure": self.api_data['main']['pressure'],
            "humidity": self.api_data['main']['humidity'],
            "clouds": self.api_data['clouds']['all'],
            "wind_speed": self.api_data['wind']['speed']
        }

        return weather

    def __get_current_location(self):
        return {
            "city": self.api_data['name'],
            "country_code": self.api_data['sys']['country'],
            "latitude": self.api_data["coord"]["lat"],
            "longitude": self.api_data["coord"]["lon"]
        }

    def forecast(self, number_days):

        url = f"{self.base_url}/forecast/daily"
        self.params["cnt"] = number_days
        response = requests.get(url, params=self.params)

        if response.status_code == 200:
            self.api_data = response.json()

            forecast = {
                "location": self.__get_forecast_location(),
                "weather_list": self.__get_forecast_weather_list()
            }

            # self.write_to_json(self.api_data, "forecast")
            self.write_to_json(forecast, "ow_forecast")

    def __get_forecast_weather_list(self):
        weather_list = []
        for day in self.api_data["list"]:
            weather = {
                "date": str(datetime.fromtimestamp(day['dt']).date()),
                'conditions': day['weather'][0]['main'],
                'description': day['weather'][0]['description'],
                'icon': day['weather'][0]['icon'],
                'temp': day['temp'],
                'feels_like': day['feels_like'],
                'pressure': day['pressure'],
                'humidity': day['humidity'],
                'clouds': day['clouds'],
                'wind_speed': day['speed'],  # m/s
                'precip_prob': float(day['pop']) * 100  # percent
            }

            weather_list.append(weather)

        return weather_list

    def __get_forecast_location(self):
        return {
            "city": self.api_data['city']['name'],
            "country_code": self.api_data['city']['country'],
            "latitude": self.api_data['city']["coord"]["lat"],
            "longitude": self.api_data['city']["coord"]["lon"]
        }



    @staticmethod
    def write_to_json(data, file_name):
        with open(f"data/{file_name}.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    start_time = time.time()


    weatherHandler = OpenWeatherAPI(50.43, 30.52)
    #
    current_weather1 = weatherHandler.current_weather()
    print(current_weather1)
    # weatherHandler.write_to_json(current_weather1, "ow_current_weather")

    # weather7 = weatherHandler.forecast(7)

    print(f"Time: {time.time() - start_time}")
