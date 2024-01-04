from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt


from flask_wrapper import FlaskAppWrapper
from views.weather.weather_handler import WeatherHandler
from views.login.login_handler import LoginHandler
from views.api_key.api_key_handler import ApiKeyHandler
from config import APP_SECRET_KEY

# Flask app
app_wrapper = FlaskAppWrapper(Flask(__name__))

# Add configs
app_wrapper.configs(MYSQL_HOST='localhost',
                    MYSQL_USER='Vartan',
                    MYSQL_PASSWORD='vartan2004',
                    MYSQL_DB='weatherwizard',
                    SECRET_KEY=APP_SECRET_KEY)

# Database
mysql = MySQL(app_wrapper.app)

# Password hashing
bcrypt = Bcrypt(app_wrapper.app)

# Allow cors
CORS(app_wrapper.app)

# Authorisation
app_wrapper.add_endpoint('/', 'index', LoginHandler.index, methods=['GET'])
app_wrapper.add_endpoint('/login', 'login', LoginHandler.login, methods=['GET', 'POST'])
app_wrapper.add_endpoint('/logout', 'logout', LoginHandler.logout, methods=['GET', 'POST'])
app_wrapper.add_endpoint('/register', 'register', LoginHandler.register, methods=['GET', 'POST'])

# Getting API key
app_wrapper.add_endpoint('/apikey', 'apikey', ApiKeyHandler.api_key, methods=['GET', 'POST'])

# Getting Weather
app_wrapper.add_endpoint('/weather', 'weather', WeatherHandler.current, methods=['GET'])
app_wrapper.add_endpoint('/forecast', 'forecast', WeatherHandler.forecast, methods=['GET'])

if __name__ == '__main__':
    app_wrapper.run(debug=True)
