import re

from flask import Flask, render_template, jsonify, request, abort
from weather_sources.data_aggregation.aggregate_data import aggregate_weather_data
from config import city_coordinates
import time

app = Flask(__name__)


@app.errorhandler(400)
def bad_request_error(error):
    # Опрацьовуємо помилку 400 тут
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400


@app.route('/')
def hello_world():  # put application's code here
    return "<h1>Main Page</h1"


@app.route('/weather/', methods=['GET'])
def weather():  # put application's code here

    lat_text = request.args.get('lat')
    lon_text = request.args.get('lon')

    print(lat_text, lon_text)

    if is_valid_lat(lat_text) and is_valid_lon(lon_text):
        lat, lon = float(lat_text), float(lon_text)
    else:
        print("Invalid coordinates!")
        abort(400, "Invalid coordinates provided")


    time_start = time.time()
    json_data = aggregate_weather_data(lat, lon)
    print("Aggregation time: ", time.time() - time_start)

    response = jsonify(json_data)

    # Додайте заголовок для вказівки клієнту, що це JSON
    response.headers.add('Content-Type', 'application/json')

    return response


def is_valid_lat(lat):
    pattern = r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$'
    return bool(re.match(pattern, lat))


def is_valid_lon(lon):
    pattern = r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$'
    return bool(re.match(pattern, lon))


if __name__ == '__main__':
    app.run()
