from io import StringIO

from bs4 import BeautifulSoup
import pandas as pd

with open("data/index.html", "r") as file:
    html_source = file.read()

soup = BeautifulSoup(html_source, "html.parser")
location = soup.find(class_="cityName cityNameShort")

city = location.find("h1").text.strip()
region = location.find(class_="currentRegion").text.strip()

current_elements = soup.find_all(class_="cur")
for element in current_elements:
    print(element)

location = {
    "city": city,
    "region": region
}

if current_elements[7].text == '-':
    precip_prob = 0
else:
    precip_prob = int(current_elements[7].text)

weather = {
    "weather_time": current_elements[0].text.replace(' ', ''),
    "condition":  current_elements[1].find('div').get("title"),
    "temp": int(current_elements[2].text[1:-1]),
    "feels_like": int(current_elements[3].text[1:-1]),
    "pressure": int(current_elements[4].text),
    "humidity": int(current_elements[5].text),
    "wind_speed": float(current_elements[6].text),
    "precip_prob": precip_prob
}

print("\nLocation:\n"
      f"City: {city}\n"
      f"Region: {region}\n")

print("Weather:\n")
for key in weather:
    print(f"{key}: {weather[key]}")

current_weather = {
    "location": location,
    "weather": weather
}
