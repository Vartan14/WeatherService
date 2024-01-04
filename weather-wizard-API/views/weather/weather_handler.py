import MySQLdb
from flask import jsonify, request, abort
from data_aggregation.current_weather import CurrentWeather
from data_aggregation.forecast import Forecast
from views.weather.validation import Validator


class WeatherHandler:
    @staticmethod
    def check_api_key(api_key):
        from app import mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM api_keys WHERE api_key = %s', (api_key,))
        existing_api_key_data = cursor.fetchone()
        return existing_api_key_data


    @classmethod
    def current(cls):

        try:
            lat, lon = Validator.validate_coords(
                request.args.get('lat'),
                request.args.get('lon'))
        except ValueError as error:
            abort(400, error)

        if cls.check_api_key(request.args.get('apikey')):
            current_weather = CurrentWeather(lat, lon)
            data = current_weather.get()

            if data is not None:
                response = jsonify(data)
                response.headers.add('Content-Type', 'application/json')
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            else:
                abort(500, f"Cannot find weather by given coordinates: lat={lat}, lon={lon}")
        else:
            abort(400, f"Invalid API key.")

    @classmethod
    def forecast(cls):
        try:
            lat, lon = Validator.validate_coords(
                request.args.get('lat'),
                request.args.get('lon'))

            days = Validator.validate_days(
                request.args.get('days'))
        except ValueError as error:
            abort(400, error)

        if cls.check_api_key(request.args.get('apikey')):

            forecast_handler = Forecast(lat, lon, days)
            data = forecast_handler.get()

            if data is not None:
                response = jsonify(data)
                response.headers.add('Content-Type', 'application/json')
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            else:
                abort(500, f"Cannot find weather by given coordinates: lat={lat}, lon={lon}")
        else:
            abort(400, f"Invalid API key.")