import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from db_config import configure_database


app = Flask(__name__)

configure_database(app=app)


# set path for environment variables file
load_dotenv(dotenv_path='.env')

# config your host & port for app using environment variable
HOST = os.environ['HOST']
PORT = os.environ['BACKEND_PORT']


# backend for all routes


@app.route('/')
def home():
    return "hello world"


# create a new review
@app.route('/new-review', methods=['POST'])
def new_review():
    return 'Create a new review'


# display all reviews
@app.route('/review/all', methods=['POST'])
def all_reviews():
    # from models import db_models
    # review = db_models.Reviews.query.first()
    # if review is None:
    #     return 'Not found'
    # else:
    #     get_reviews = db_models.Reviews.query.all()
    #     return render_template('searchReviewPage.html', get_reviews=get_reviews)
    return "all reviews"



# display all review locations
@app.route('/review/locations', methods=['POST'])
def find_locations():
    return 'Find all locations'


# display all reviews by rating 
@app.route('/review/rating', methods=['POST'])
def find_by_rating():
    rating = request.form['searchRating']
    return f'Find all reviews with a rating of {rating}'


# display reviews by door number
@app.route('/review/door', methods=['POST'])
def find_by_door():
    door = request.form['searchDoorNum']
    return f'Find all reviews with door number: {door}'


# display reviews by street name
@app.route('/review/street', methods=['POST'])
def find_by_street():
    street = request.form['searchStreetName']
    return f'Find all reviews with the same location as: {street}'


# display reviews by location
@app.route('/review/location', methods=['POST'])
def find_by_location():
    location = request.form['searchLocation']
    return f'Find all reviews with the same location as: {location}'


# display reviews by postcode
@app.route('/review/postcode', methods=['POST'])
def find_by_postcode():
    postcode = request.form['searchPostcode']
    return f'Find all reviews with the same review as: {postcode}'



if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
    