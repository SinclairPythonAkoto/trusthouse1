import os
import folium
from trusthouse import app
from trusthouse.extensions import init_db, SessionLocal
from flask import render_template, request
from trusthouse.models import Maps, Business, Incident
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
load_dotenv()

init_db()

# Configure the app with the db object
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TRUSTHOUSE_DB']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# config your host & port for app using environment variable
HOST = os.environ['HOST']
PORT = os.environ['MAP_SERVICE_PORT']


# create routes
@app.route('/map')
def trusthouse_map():
    coordinates = Maps.query.all()
    business_data = Business.query.all()
    incident_reports = Incident.query.all()
    longitude = '-0.1244477'
    latitude = '51.4994252'
    location = float(latitude), float(longitude)
    map = folium.Map(
        location=location,
        tiles='Stamen Terrain',
        zoom_start=9,
    )
    geolocator = Nominatim(user_agent='geoapiExercises')
    for geocode in coordinates:
        long = geocode.lon
        lat = geocode.lat
        # get street name from latitude & longitude
        street_location = geolocator.reverse(f'{lat},{long}')
        street_location = str(street_location)
        data = street_location.split(',')

        # adding the points to the map
        folium.Marker(
            location=[float(lat), float(long)],
            popup=f'{data[0]},\n{geocode.location.postcode.upper()}',
            tooltip='check address',
            icon=folium.Icon(color='red', icon='home', prefix='fa') 
        ).add_to(map)

    # add buisness markers to map
    for trusthouse_map in coordinates:
        for buisness in business_data:
            if trusthouse_map.address_id == buisness.address_id:
                folium.Marker(
                    location=[float(trusthouse_map.lat), float(trusthouse_map.lon)],
                    popup=f'{buisness.name.upper()},\n{buisness.category},\n{buisness.contact},\n{buisness.place.postcode.upper()}',
                    tooltip='View Buisness',
                    icon=folium.Icon(color='green', icon='gbp', prefix='fa')
                ).add_to(map)

    return map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)