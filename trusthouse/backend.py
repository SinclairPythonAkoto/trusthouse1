import os
from trusthouse import app
from trusthouse.extensions import init_db, SessionLocal
from flask import render_template, request
from trusthouse.models import Reviews, Address
from trusthouse.utils import (
    validate_door_request,
    validate_rating_request,
    validate_postcode_request,
    validate_street_request,
    validate_location_request, 
    create_new_address, 
    get_postcode_coordinates, 
    create_new_map, 
    create_new_review, 
    error_message, ok_message, warning_message
    )
from dotenv import load_dotenv
load_dotenv()

init_db()

# Configure the app with the db object
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TRUSTHOUSE_DB']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# config your host & port for app using environment variable
HOST = os.environ['HOST']
PORT = os.environ['BACKEND_PORT']


# create a new review
@app.route('/new-review', methods=['POST'])
def new_review():
    # address data
    door = request.form['propertyNumber']
    street_name = request.form['streetName']
    town_city = request.form['town_city']
    postcode = request.form['postcode']
    # review data
    review_rating = request.form['rating']
    review_rating = int(review_rating)
    review_text = request.form['reviewText']
    review_type = request.form['selection']

    # get data to check if new review already exists
    check_door = validate_door_request(door)
    check_postcode = validate_postcode_request(postcode)
    if check_postcode == False:
        new_address = create_new_address(
            door.lower(),
            street_name.lower(),
            town_city.lower(),
            postcode.lower(),
        )
        # get latitude & logitude from user postcode
        user_postcode_coordinates = get_postcode_coordinates(postcode)
        # if there is NOT an existing latitude & longitude
        if user_postcode_coordinates == []:
            message = warning_message()[0]['Warning']
            return render_template('writeReviewPage.html', message=message)
        # if there IS existing longitute & latitude
        elif user_postcode_coordinates:
            latitude = user_postcode_coordinates[0].get('lat')
            longitude = user_postcode_coordinates[0].get('lon')
            print(longitude, latitude, new_address)
            create_new_map(longitude, latitude, new_address)
            create_new_review(review_rating, review_text, review_type, new_address)
            message = ok_message()[1]['Success']
            return render_template('writeReviewPage.html', message=message)
        else:
            message = error_message()[0]['Error']
            return render_template('writeReviewPage.html', message=message)
    else:
        if (check_door == False or True) and check_postcode == True:
            new_address = create_new_address(
                door.lower(),
                street_name.lower(),
                town_city.lower(),
                postcode.lower(),
            )
            user_postcode_coordinates = get_postcode_coordinates(postcode)
            create_new_review(review_rating, review_text, review_type, new_address)
            message = ok_message()[1]['Success']
            return render_template('writeReviewPage.html', message=message)


# display all reviews
@app.route('/review/all', methods=['POST'])
def all_reviews():
    session = SessionLocal()
    review = session.query(Reviews).first()
    if review is None:
        return 'No Reviews found.'
    else:
        get_reviews = session.query(Reviews).all()
        return render_template('searchReviewPage.html', get_reviews=get_reviews)



# display all review locations
@app.route('/review/all/locations', methods=['POST'])
def find_locations():
    session = SessionLocal()
    location = session.query(Address).first()
    if location is None:
        return 'No Location found.'
    listed_locations = session.query(Address).all()
    return render_template('searchReviewPage.html', listed_locations=listed_locations)



# display all reviews by rating 
@app.route('/review/rating', methods=['POST'])
def find_by_rating():
    session = SessionLocal()
    user_rating_request = request.form['searchRating']
    user_rating_request = int(user_rating_request)
    response = validate_rating_request(user_rating_request)
    if response == False:
        void = error_message()[1]['Error']
        return render_template('searchReviewPage.html', void=void)
    get_ratings = session.query(Reviews).filter_by(rating=user_rating_request).all()
    return render_template('searchReviewPage.html', get_ratings=get_ratings)



# display reviews by door number
@app.route('/review/door', methods=['POST'])
def find_by_door():
    session = SessionLocal()
    user_door_request = request.form['searchDoorNum']
    response = validate_door_request(user_door_request)
    if response == False:
        void = error_message()[1]['Error']
        return render_template('searchReviewPage.html', void=void)
    filter_door = session.query(Reviews).all()
    return render_template(
        'searchReviewPage.html',
        user_door_request=user_door_request,
        filter_door=filter_door,
    )



# display reviews by street name
@app.route('/review/street', methods=['POST'])
def find_by_street():
    user_street_request = request.form['searchStreetName']
    response = validate_street_request(user_street_request)
    if response == False:
        void = error_message()[1]['Error']
        return render_template('searchReviewPage.html', void=void)
    filter_street = Reviews.query.all()
    return render_template(
        'searchReviewPage.html',
        user_street_request=user_street_request,
        filter_street=filter_street,
    )




# display reviews by location
@app.route('/review/location', methods=['POST'])
def find_by_location():
    user_location_request = request.form['searchLocation']
    response = validate_location_request(user_location_request)
    if response == False:
        void = error_message()[1]['Error']
        return render_template('searchReviewPage.html', void=void)
    filter_location = Reviews.query.all()
    return render_template(
        'searchReviewPage.html',
        user_location_request=user_location_request,
        filter_location=filter_location,
    )



# display reviews by postcode
@app.route('/review/postcode', methods=['POST'])
def find_by_postcode():
    user_postcode_request = request.form['searchPostcode']
    response = validate_postcode_request(user_postcode_request)
    if response == False:
        void = error_message()[1]['Error']
        return render_template('searchReviewPage.html', void=void)
    filter_postcode = Reviews.query.all()
    return render_template(
        'searchReviewPage.html',
        user_postcode_request=user_postcode_request,
        filter_postcode=filter_postcode,
    )



if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
    