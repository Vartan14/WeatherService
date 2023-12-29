import asyncio
import json
import time
import numpy as np

from config import city_coordinates, MAX_DAYS_FORECAST, MIN_DAYS_FORECAST
from weather_sources.open_weather_api.open_weather import OpenWeatherAPI
from weather_sources.sinoptik.sinoptik_web_scraper import SinoptikWebScraper
from weather_sources.visual_crossing.visual_crossing import VisualCrossingAPI


class Forecast:
    def __init__(self, lat, lon, days):
        self.lat = lat
        self.lon = lon
        self.days = days

    def get(self):
        data = asyncio.run(self.__get_data())

        # remove None sources from list
        if None in data:
            data = [source for source in data if source is not None]

        # return None if no weather
        if len(data) == 0:
            return None

        weather_list = []
        temp_keys = list(data[0]["weather_list"][0]["temp"].keys())
        feels_like_keys = list(data[0]["weather_list"][0]["feels_like"].keys())

        for i in range(self.days):
            temp = {
                day_time: self.__aggregate_temp(data, i, "temp", day_time) for day_time in temp_keys
            }
            feels_like = {
                day_time: self.__aggregate_temp(data, i, "feels_like", day_time) for day_time in feels_like_keys
            }

            weather = {
                "date": f"/".join([source['weather_list'][i]['date'] for source in data]),
                "condition": data[0]["weather_list"][i].get("condition"),
                "desc": data[0]["weather_list"][i].get("desc"),
                "icon": data[0]["weather_list"][i].get("icon"),
                "temp": temp,
                "feels_like": feels_like,
                "pressure": self.__aggregate_prop(data, i, "pressure"),
                "humidity": self.__aggregate_prop(data, i, "humidity"),
                "wind_speed": self.__aggregate_prop(data, i, "wind_speed", 2),
                "clouds": self.__aggregate_prop(data, i, "clouds"),
                "precip_prob": self.__aggregate_prop(data, i, "precip_prob")
            }

            weather_list.append(weather)

        aggregated_weather_data = {
            "location": data[0]["location"],
            "weather_list": weather_list
        }

        with open("data/aggregated_forecast.json", "w") as file:
            json.dump(aggregated_weather_data, file, indent=4, ensure_ascii=False)

        return aggregated_weather_data

    async def __get_data(self):
        weather1 = OpenWeatherAPI(self.lat, self.lon)
        weather2 = VisualCrossingAPI(self.lat, self.lon)
        weather3 = SinoptikWebScraper(self.lat, self.lon)

        tasks = [asyncio.create_task(weather1.forecast(self.days)),
                 asyncio.create_task(weather2.forecast(self.days)),
                 asyncio.create_task(weather3.forecast(self.days))]

        results = await asyncio.gather(*tasks)

        return results

    @staticmethod
    def __aggregate_temp(data, i, type_, day_time):
        agg_data = [source["weather_list"][i][type_][day_time] for source in data if source is not None]
        if any(agg_data):
            agg_prop = np.mean(agg_data)
            return round(agg_prop, 2)

    @staticmethod
    def __aggregate_prop(data, i, prop, round_number=0):
        agg_data = [source["weather_list"][i].get(prop) for source in data if source is not None]
        if any(agg_data):
            agg_prop = np.mean([data for data in agg_data if data is not None])
            return round(agg_prop, round_number) if round_number else round(agg_prop)


if __name__ == '__main__':
    start_time = time.time()

    weather_handler = Forecast(*city_coordinates["Lyon"], 7)

    weather_handler.get()

    print(f"Time: {time.time() - start_time}")
