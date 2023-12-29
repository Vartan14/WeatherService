from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS
from weather_sources.data_aggregation.current_weather import CurrentWeather
from weather_sources.data_aggregation.forecast import Forecast
from validation import Validator
from config import city_coordinates
import time

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "<h1>Weather Wizard API</h1"


@app.route('/weather', methods=['GET'])
def weather():
    try:
        lat, lon = Validator.validate_coords(
            request.args.get('lat'),
            request.args.get('lon'))
    except ValueError as error:
        abort(400, error)

    current_weather = CurrentWeather(lat, lon)
    data = current_weather.get()

    if data is not None:
        response = jsonify(data)
        response.headers.add('Content-Type', 'application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        abort(500, f"Cannot find weather by given coordinates: lat={lat}, lon={lon}")


@app.route('/forecast', methods=['GET'])
def forecast():
    try:
        lat, lon = Validator.validate_coords(
            request.args.get('lat'),
            request.args.get('lon'))

        days = Validator.validate_days(
            request.args.get('days'))
    except ValueError as error:
        abort(400, error)

    forecast_handler = Forecast(lat, lon, days)
    data = forecast_handler.get()

    if data is not None:
        response = jsonify(data)
        response.headers.add('Content-Type', 'application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        abort(500, f"Cannot find weather by given coordinates: lat={lat}, lon={lon}")


@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server Error', 'message': str(error)}), 500


if __name__ == '__main__':
    app.run(debug=True)
