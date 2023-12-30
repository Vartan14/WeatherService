from flask import jsonify, request, abort
from data_aggregation.current_weather import CurrentWeather
from data_aggregation.forecast import Forecast
from handlers.validation import Validator


class WeatherHandler:
    @staticmethod
    def hello_world():
        return "<h1>Weather Wizard API</h1"

    @staticmethod
    def current():
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

    @staticmethod
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
