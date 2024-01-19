import asyncio
import numpy as np
from data_sources.open_weather_api.open_weather import OpenWeatherAPI
from data_sources.visual_crossing.visual_crossing import VisualCrossingAPI
from data_sources.sinoptik.sinoptik_web_scraper import SinoptikWebScraper
import time
import json
from config import city_coordinates


class CurrentWeather:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def get(self):
        data = asyncio.run(self.__get_data())

        # remove None sources from list
        if None in data:
            data = [source for source in data if source is not None]

        # return None if no weather
        if len(data) == 0:
            return None

        weather = {
            "time": f"/".join([source['weather']['time'] for source in data]),
            "condition": data[0]["weather"].get("condition"),
            "desc": data[0]["weather"].get("desc"),
            "icon": data[0]["weather"].get("icon"),

            "temp": self.__aggregate_prop(data, "temp", 2),  # temp in Celsius
            "feels_like": self.__aggregate_prop(data, "feels_like", 2),  # feels_like temp in Celsius

            "pressure": round(self.__aggregate_prop(data, "pressure") / 1.33333),  # pressure in mm
            "humidity": self.__aggregate_prop(data, "humidity"),  # humidity in %
            "wind_speed": self.__aggregate_prop(data, "wind_speed", 2),  # wind speed in m/s
            "clouds": self.__aggregate_prop(data, "clouds"),  # clouds in %
            "precip_prob": self.__aggregate_prop(data, "precip_prob", ),  # precipitation probability in %
        }

        aggregated_weather_data = {
            "location": data[0]["location"],
            "weather": weather
        }

        with open("data/aggregated_data.json", "w") as file:
            json.dump(aggregated_weather_data, file, indent=4, ensure_ascii=False)

        return aggregated_weather_data

    async def __get_data(self):
        weather1 = OpenWeatherAPI(self.lat, self.lon)
        weather2 = VisualCrossingAPI(self.lat, self.lon)
        weather3 = SinoptikWebScraper(self.lat, self.lon)

        tasks = [asyncio.create_task(weather1.current_weather()),
                 asyncio.create_task(weather2.current_weather()),
                 asyncio.create_task(weather3.current_weather())]

        results = await asyncio.gather(*tasks)

        return results

    @staticmethod
    def __aggregate_prop(data, prop, round_number=0):
        agg_data = [source["weather"].get(prop) for source in data if source is not None]

        if any(agg_data):
            aggregated_prop = np.mean([data for data in agg_data if data is not None])
            return round(aggregated_prop, round_number) if round_number else round(aggregated_prop)


if __name__ == '__main__':
    start_time = time.time()

    CurrentWeather(*city_coordinates["Vinn"]).get()

    print(f"Time: {time.time() - start_time}")
