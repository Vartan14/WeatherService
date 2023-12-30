from flask import Flask
from flask_cors import CORS
from flask_wrapper import FlaskAppWrapper
from handlers.weather_handler import WeatherHandler


class Server:
    def __init__(self):
        # create Flask app
        self.app_wrapper = FlaskAppWrapper(Flask(__name__))
        CORS(self.app_wrapper.app)
        # Add endpoints
        self.app_wrapper.add_endpoint('/', 'hello_world', WeatherHandler.hello_world)
        self.app_wrapper.add_endpoint('/weather', 'weather', WeatherHandler.current, methods=['GET'])
        self.app_wrapper.add_endpoint('/forecast', 'forecast', WeatherHandler.forecast, methods=['GET'])

    def start(self):
        self.app_wrapper.run(debug=True)


if __name__ == '__main__':
    server = Server()
    server.start()
