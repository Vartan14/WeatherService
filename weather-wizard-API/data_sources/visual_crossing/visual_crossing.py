import asyncio
import json
import time
from aiohttp import ClientSession
from datetime import datetime, timedelta
from config import VISUAL_CROSSING_API_KEY, VISUAL_CROSSING_URL


class VisualCrossingAPI:
    def __init__(self, latitude, longitude):
        self.url = f"{VISUAL_CROSSING_URL}/{latitude},{longitude}"
        self.params = {
            'key': VISUAL_CROSSING_API_KEY,
            'unitGroup': 'metric',
        }
        self.api_data = None

    async def current_weather(self):
        async with ClientSession() as session:
            current_datetime = datetime.now()
            date = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")

            self.params['include'] = "current"

            async with session.get(f"{self.url}/{date}", params=self.params) as response:

                try:
                    if response.status == 200:
                        self.api_data = await response.json()

                        current_weather = {
                            "location": self.__get_current_location(),
                            "weather": self.__get_current_weather()
                        }

                        self.write_to_json(current_weather, "vc_cur")

                        return current_weather
                    else:
                        raise Exception(f"bad request with status code {response.status}")

                except Exception as error:
                    print(f"Visual Crossing API weather data fetching error: {error}")

    def __get_current_location(self):
        return {
            'timezone_city': self.api_data['timezone'],
            'latitude': self.api_data['latitude'],
            'longitude': self.api_data['longitude'],
        }

    def __get_current_weather(self):
        return {
            'time':
                f"{self.api_data['currentConditions']['datetime']}",
            'desc': self.api_data['currentConditions']['conditions'],
            'temp': self.api_data['currentConditions']['temp'],
            'feels_like': self.api_data['currentConditions']['feelslike'],
            'pressure': self.api_data['currentConditions']['pressure'],
            'humidity': self.api_data['currentConditions']['humidity'],
            'clouds': self.api_data['currentConditions']['cloudcover'],
            'wind_speed': round(self.api_data['currentConditions']['windspeed'] / 3.6, 2),  # m/s
            'precip_prob': self.api_data['currentConditions']['precipprob']  # Probability of precipitation
        }

    async def forecast(self, number_days):
        async with ClientSession() as session:
            current_datetime = datetime.now()
            forecast_datetime = current_datetime + timedelta(days=number_days - 1)

            date_1 = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            date_2 = forecast_datetime.strftime("%Y-%m-%dT%H:%M:%S")

            async with session.get(f"{self.url}/{date_1}/{date_2}", params=self.params) as response:

                try:
                    if response.status == 200:
                        self.api_data = await response.json()

                        forecast = {
                            "location": self.__get_current_location(),
                            "weather_list": self.__get_weather_list()
                        }
                        self.write_to_json(forecast, 'vc_forecast')

                        return forecast

                    else:
                        raise Exception(f"bad request with status code {response.status}")

                except Exception as error:
                    print(f"Visual Crossing API forecast data fetching error: {error}")

    def __get_weather_list(self):
        weather_list = []
        for day in self.api_data["days"]:
            weather = {
                'date': day['datetime'],
                'condition': day['conditions'],
                "temp": {
                    "night": day['hours'][2]['temp'],
                    "morn": day['hours'][8]['temp'],
                    "day": day['hours'][14]['temp'],
                    "eve": day['hours'][20]['temp'],
                    "min": day['tempmin'],
                    "max": day['tempmax']
                },
                "feels_like": {
                    "night": day['hours'][2]['feelslike'],
                    "morn": day['hours'][8]['feelslike'],
                    "day": day['hours'][14]['feelslike'],
                    "eve": day['hours'][20]['feelslike'],
                },
                'pressure': day['pressure'],
                'humidity': day['humidity'],
                'clouds': day['cloudcover'],
                'wind_speed': round(day['windspeed'] / 3.6, 2),
                'precip_prob': day['precipprob']
            }

            weather_list.append(weather)

        return weather_list

    @staticmethod
    def write_to_json(data, file_name):
        with open(f"data/{file_name}.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


async def main():
    start_time = time.time()

    lat, lon = city_coordinates['Vlad']

    visual_crossing = VisualCrossingAPI(lat, lon)
    # data = visual_crossing.forecast(7)

    task = asyncio.create_task(visual_crossing.forecast(7))

    await task

    # current_datetime = datetime.now()
    # date = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    # print(current_datetime + timedelta(days=2))
    print(f"Time: {(time.time() - start_time)}")


if __name__ == '__main__':
    from config import city_coordinates

    asyncio.run(main())
