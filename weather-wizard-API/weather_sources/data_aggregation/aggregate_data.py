import asyncio
import numpy as np
from weather_sources.open_weather_api.open_weather import OpenWeatherAPI
from weather_sources.visual_crossing.visual_crossing import VisualCrossingAPI
from weather_sources.sinoptik.sinoptik_web_scraper import SinoptikWebScraper
import time
import json
from config import city_coordinates


async def get_weather_data(lat, lon):
    weather1 = OpenWeatherAPI(lat, lon)
    weather2 = VisualCrossingAPI(lat, lon)
    weather3 = SinoptikWebScraper(lat, lon)

    tasks = []
    tasks.append(asyncio.create_task(weather1.current_weather()))
    tasks.append(asyncio.create_task(weather2.current_weather()))
    tasks.append(asyncio.create_task(weather3.current_weather()))

    results = await asyncio.gather(*tasks)

    return results


def aggregate(data, prop, round_number=0):
    aggregated_prop = np.mean([source["weather"][prop] for source in data])
    return round(aggregated_prop, round_number) if round_number else round(aggregated_prop)


def aggregate_weather_data(lat, lon):
    data = asyncio.run(get_weather_data(lat, lon))

    # remove from list None sources
    data = [source for source in data if source]

    location = data[0]["location"]

    weather = {
        "time": f"/".join([source['weather']['time'] for source in data]),
        "condition": data[0]["weather"]["condition"],
        "desc": data[1]["weather"]["desc"],

        # temp in Celsius
        "temp": aggregate(data, "temp", 2),

        # feels_like temp in Celsius
        "feels_like": aggregate(data, "feels_like", 2),

        # pressure in hPa
        "pressure": aggregate(data, "pressure"),

        # humidity in %
        "humidity": aggregate(data, "humidity"),

        # wind speed in m/s
        "wind_speed": aggregate(data, "wind_speed", 2),

        # clouds in %
        "clouds": aggregate(data[:-1], "clouds"),

        # precipitation probability in %
        "precip_prob": aggregate(data[1:], "precip_prob", ),
    }

    aggregated_weather_data = {
        "location": location,
        "weather": weather
    }

    with open("data/aggregated_data.json", "w") as file:
        json.dump(aggregated_weather_data, file, indent=4, ensure_ascii=False)

    return aggregated_weather_data

if __name__ == '__main__':

    start_time = time.time()
    # weather1 = OpenWeatherAPI(50.43, 30.52)
    # weather2 = VisualCrossingAPI(50.43, 30.52)
    # # weather3 = SinoptikWebScraper(50.43, 30.52)
    # #
    # weather1.forecast(1)
    # weather2.forecast(1)
    #weather2.current_weather()
    # weather3.current_weather()

    lat, lon = city_coordinates["Moh"]
    #print(f"Latitude: {lat}, Longitude: {lon}")
    aggregate_weather_data(lat, 111)

    print(f"Time: {time.time() - start_time}")