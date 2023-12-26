import requests
import json
from config import OPEN_WEATHER_API_KEY


url = "http://api.openweathermap.org/geo/1.0/reverse"

params = {
    "lat": 48.44,
    "lon": 27.80,
    "appid": OPEN_WEATHER_API_KEY,
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print(response.json())
    with open("weather_sources.json", "w") as outfile:
        json.dump(response.json(), outfile)