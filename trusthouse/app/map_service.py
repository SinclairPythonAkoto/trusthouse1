import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import folium 
from geopy.geocoders import Nominatim


app = Flask(__name__)

# set path for environment variables file
load_dotenv(dotenv_path='.env')

# config your host & port for app using environment variable
HOST = os.environ['HOST']
PORT = os.environ['MAP_SERVICE_PORT']


@app.route('/')
def trust_map():
    return 'show map'

# backend for all routes


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)