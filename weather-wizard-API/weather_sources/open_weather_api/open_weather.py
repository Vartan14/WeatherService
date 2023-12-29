import asyncio
import time
import json
from config import OPEN_WEATHER_API_KEY, OPEN_WEATHER_URL, city_coordinates
from datetime import datetime
from aiohttp import ClientSession


class OpenWeatherAPI:
    def __init__(self, latitude, longitude):
        self.base_url = OPEN_WEATHER_URL
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
                try:
                    if response.status == 200:
                        self.api_data = await response.json()

                        current_weather = {
                            "location": self.__get_current_location(),
                            "weather": self.__get_current_weather()
                        }

                        self.write_to_json(current_weather, "ow_cur")

                        return current_weather

                    else:
                        raise Exception(f"bad request with status: {response.status}")

                except Exception as error:
                    print(f"Open Weather API weather data fetching error: {error}")

    def __get_current_weather(self):
        weather = {
            # weather time
            "time": str(datetime.fromtimestamp(self.api_data["dt"]).time()),
            # weather description
            "condition": self.api_data['weather'][0]['main1'],
            "desc": self.api_data['weather'][0]['description'].capitalize(),
            "icon": self.api_data['weather'][0]['icon'],

            # temperature in Celsius
            "temp": self.api_data['main']['temp'],
            "feels_like": self.api_data['main']['feels_like'],

            # other properties
            "pressure": self.api_data['main']['pressure'],
            "humidity": self.api_data['main']['humidity'],
            "clouds": self.api_data['clouds']['all'],
            "wind_speed": self.api_data['wind']['speed']
        }

        return weather

    def __get_current_location(self):
        return {
            "city": self.api_data.get('name'),
            "country_code": self.api_data['sys'].get('country'),
            "latitude": self.api_data["coord"]["lat"],
            "longitude": self.api_data["coord"]["lon"]
        }

    async def forecast(self, number_days):
        async with ClientSession() as session:
            url = f"{self.base_url}/forecast/daily"
            self.params["cnt"] = number_days

            async with session.get(url, params=self.params) as response:
                try:
                    if response.status == 200:
                        self.api_data = await response.json()

                        forecast = {
                            "location": self.__get_forecast_location(),
                            "weather_list": self.__get_forecast_weather_list()
                        }

                        self.write_to_json(forecast, "ow_forecast")
                        return forecast

                    else:
                        raise Exception(f"bad request with status: {response.status}")

                except Exception as error:
                    print(f"Open Weather API forecast fetching error: {error}")

    def __get_forecast_weather_list(self):
        weather_list = []
        for day in self.api_data["list"]:
            weather = {
                "date": str(datetime.fromtimestamp(day['dt']).date()),
                'condition': day['weather'][0]['main'],
                'desc': day['weather'][0]['description'].capitalize(),
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
            "city": self.api_data['city'].get('name'),
            "country_code": self.api_data['city'].get('country'),
            "latitude": self.api_data['city']["coord"]["lat"],
            "longitude": self.api_data['city']["coord"]["lon"]
        }

    @staticmethod
    def write_to_json(data, file_name):
        with open(f"data/{file_name}.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


async def main():
    start_time = time.time()

    weather_handler = OpenWeatherAPI(1, 1)
    # data = visual_crossing.forecast(7)

    task = asyncio.create_task(weather_handler.current_weather())

    await task

    print(f"Time: {(time.time() - start_time)}")


if __name__ == "__main__":
    asyncio.run(main())
