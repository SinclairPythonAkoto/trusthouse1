import os
from dotenv import load_dotenv
from flask import Flask, render_template
load_dotenv()


front_app = Flask(__name__)


# config your host & port for app using environment variables
HOST = os.environ['HOST']
PORT = os.environ['FRONTEND_PORT']


# define all routes

# landing page
@front_app.route('/')
def index():
    return render_template('index.html')


# homepage
@front_app.route('/home')
def home():
    return render_template('homepage.html')


# Trust House API information page
@front_app.route('/trutshouse/api/info')
def trusthouse_api_info():
    return render_template('trustHouseAPI.html')


# create a new review
@front_app.route('/new-review')
def new_review():
    return render_template('writeReviewPage.html')


# view reviews
@front_app.route('/reviews')
def find_review():
    return render_template('searchReviewPage.html')


# new_address address/new
@front_app.route('/address/new')
def new_address():
    return render_template('newAddress.html')

if __name__ == '__main__':
    front_app.run(debug=True, host=HOST, port=PORT)