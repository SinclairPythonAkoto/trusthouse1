import os
import requests
from typing import List, Dict
from trusthouse import app
from trusthouse.extensions import init_db, SessionLocal
from trusthouse.models import Address, Reviews
from trusthouse.utils import (
    ok_message, 
    error_message,
    validate_door_request,
    validate_street_request,
    validate_postcode_request,
    validate_rating_request,
    validate_location_request,
    get_postcode_coordinates,
    warning_message,
) 
from flask import jsonify
from dotenv import load_dotenv
load_dotenv()

init_db()

# Configure the app with the db object
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TRUSTHOUSE_DB']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# config your host & port for app using environment variable
HOST: str = os.environ['HOST']
PORT: int = os.environ['API_PORT']


# create api routes

# instructions / manual
@app.route('/')
def api_home() -> Dict:
    manual: Dict = {
        'APP': 'TrustHouse API',
        'DESCRIPTION': 'This will be the manual or instructions on how to use the API.',
        'STATUS': ok_message()[3]
    }
    return jsonify(manual)

# display all address API
@app.route('/api/display/addresses')
def display_address_api() -> Dict:
    session: SessionLocal = SessionLocal()
    check_address: Reviews = session.query(Address).first()
    if check_address is None:
        return jsonify(error_message()[2])
    all_addresses: List[Reviews] = session.query(Address).all()
    db_query_result: List[Dict] = []
    for address in all_addresses:
        result = {
                'id': address.id,
                'Door Number': address.door_num,
                'Street Name': address.street,
                'Location': address.location,
                'Postcode': address.postcode,
        }
        db_query_result.append(result)
    data: Dict = {
        'Status': ok_message()[3],
        'Search all addresses': ok_message()[2],
        'Display Addresses': db_query_result,
    }
    return jsonify(data)


# display all reviews API
@app.route('/api/display/reviews')
def display_reviews_api() -> Dict:
    session: SessionLocal = SessionLocal()
    check_review: Reviews = session.query(Reviews).first()
    if check_review is None:
        return jsonify(error_message()[2])
    all_reviews: List[Reviews] = session.query(Reviews).all()
    review_result: List[Dict] = []
    for review in all_reviews:
        result = {
            'id': review.id,
            'Rating': review.rating,
            'Review': review.review,
            'Type': review.type,
            'Date': review.date,
            'Address ID': review.address_id,
            'Address': {
                'id': review.address.id,
                'Door Number': review.address.door_num,
                'Street': review.address.street,
                'Postode': review.address.postcode,
            },
        }
        review_result.append(result)
    data: Dict = {
        'Status': ok_message()[3],
        'Search all reviews': ok_message()[2],
        'Display Reviews': review_result, 
    }
    return jsonify(data)


# display review by door number API
@app.route('/api/door/<door>')
def filter_door_api(door: str) -> Dict:
    session: SessionLocal = SessionLocal()
    user_door_request: str = door
    response: bool = validate_door_request(door)
    if response is False:
        void: Dict = {
            'Search by door number': error_message()[1],
            'Status': error_message()[2],
        }
        return jsonify(void)
    user_door_result: List[Dict] = []
    get_reviews: List[Reviews]  = session.query(Reviews).all()
    for review in get_reviews:
        if user_door_request == review.address.door_num:
            db_result = {
                'id': review.id,
                'Rating': review.rating,
                'Review': review.review,
                'Type': review.type,
                'Date': review.date,
                'Address ID': review.address_id,
                'Address': {
                    'id': review.address.id,
                    'Door Number': review.address.door_num,
                    'Street': review.address.street,
                    'Postode': review.address.postcode,
                },
            }
            user_door_request.append(db_result)
        data: Dict = {
            'Status': ok_message()[3],
            'Search by door number': ok_message()[2],
            'Reviews by door number': user_door_result, 
        }
        return jsonify(data)


# display review by street name API
@app.route('/api/street/<street>')
def filter_street_api(street) -> Dict:
    session: SessionLocal = SessionLocal()
    user_street_request: str = street
    response: bool = validate_street_request(user_street_request)
    if response is False:
        void: Dict = {
            'Search by street name': error_message()[1],
            'Status': error_message()[2],
        }
        return jsonify(void)
    user_street_restult: List[Dict] = []
    get_reviews: List[Reviews] = session.query(Reviews).all()
    for review in get_reviews:
        if user_street_request == review.address.street:
            result = {
                'id': review.id,
                'Rating': review.rating,
                'Review': review.review,
                'Type': review.type,
                'Date': review.date,
                'Address ID': review.address_id,
                'Address': {
                    'id': review.address.id,
                    'Door Number': review.address.street,
                    'Street': review.address.street,
                    'Postode': review.address.postcode,
                },
            }
            user_street_restult.append(result)
    data: Dict = {
        'Status': ok_message()[3],
        'Search by street name': ok_message()[2],
        'Reviews by street name': user_street_restult,
    }
    return jsonify(data)



# display review by postcode API
@app.route('/api/postcode/<postcode>')
def filter_postcode_api(postcode) -> Dict:
    session: SessionLocal = SessionLocal()
    user_postcode: str = postcode
    response: bool = validate_postcode_request(user_postcode)
    if response is False:
        void: Dict = {
            'Search by postcode': error_message()[1],
            'Status': error_message()[2]
        }
        return jsonify(void)
    user_postcode_result: List[Dict] = []
    get_reviews: List[Reviews] = session.query(Reviews).all()
    for review in get_reviews:
        if user_postcode == review.address.postcode:
            result = {
                'id': review.id,
                'Rating': review.rating,
                'Review': review.review,
                'Type': review.type,
                'Date': review.date,
                'Address ID': review.address_id,
                'Address': {
                    'id': review.address.id,
                    'Door Number': review.address.street,
                    'Street': review.address.street,
                    'Postode': review.address.postcode,
                },
            }
            user_postcode_result.append(result)
        data: Dict = {
            'Status': ok_message()[3],
            'Search by postcode': ok_message()[2],
            'Reviews by postcode': user_postcode_result,   
        }
        return jsonify(data)


# display review by rating API
@app.route('/api/rating/<rating>')
def filter_rating_api(rating) -> Dict:
    session: SessionLocal = SessionLocal()
    user_rating_request: int = int(rating)
    response: bool = validate_rating_request(user_rating_request)
    if response is False:
        void: Dict = {
            'Search review by rating': error_message()[1],
            'Status': error_message()[2],
        }
        return jsonify(void)
    user_rating_result: List[Dict] = []
    get_reviews: List[Reviews] = session.query(Reviews).all()
    for review in get_reviews:
        if user_rating_request == review.rating:
            result = {
                'id': review.id,
                'Rating': review.rating,
                'Review': review.review,
                'Type': review.type,
                'Date': review.date,
                'Address ID': review.address_id,
                'Address': {
                    'id': review.address.id,
                    'Door Number': review.address.door_num,
                    'Street': review.address.street,
                    'Postode': review.address.postcode,
                },
            }
            user_rating_result.append(result)
        data: Dict = {
            'Status': ok_message()[3],
            'Search by review rating': ok_message()[2],
            'Reviews by rating': user_rating_result, 
        }
        return jsonify(data)




# display reviews by tenant API
@app.route('/api/tenants')
def filter_tenants_api() -> Dict:
    session: SessionLocal = SessionLocal()
    check_tenant: Reviews = session.query(Reviews).filter_by(type='tenant').first()
    if check_tenant is None:
        void: Dict = {
            'Search review by tenant': error_message()[1],
            'Status': error_message()[2],
        }
        return jsonify(void)
    all_reviews: List[Reviews] = session.query(Reviews).filter_by(type='tenant').all()
    tenant_results: List[Dict] = []
    for review in all_reviews:
        result = {
            'id': review.id,
            'Rating': review.rating,
            'Review': review.review,
            'Type': review.type,
            'Date': review.date,
            'Address ID': review.address_id,
            'Address': {
                'id': review.address.id,
                'Door Number': review.address.door_num,
                'Street': review.address.street,
                'Postode': review.address.postcode,
            },
        }
        tenant_results.append(result)
    data = {
        'Status': ok_message()[3],
        'Search reviews by tenants': ok_message()[2],
        'Reviews by tenants': tenant_results,  
    }
    return jsonify(data)


# disply reviews by neighbour API
@app.route('/api/neighbours', methods=['POST'])
def filter_neighbour_api() -> Dict:
    session: SessionLocal = SessionLocal()
    check_neighbour: Reviews = session.query(Reviews).filter_by(type='neighbour').first()
    if check_neighbour is None:
        void: Dict = {
            'Search review by neighbour': error_message()[1],
            'Status': error_message()[2],
        }
        return jsonify(void)
    all_reviews: List[Reviews] = session.query(Reviews).filer_by(type='neighbour').all()
    neighbour_results: List[Dict] = []
    for review in all_reviews:
        result = {
            'id': review.id,
            'Rating': review.rating,
            'Review': review.review,
            'Type': review.type,
            'Date': review.date,
            'Address ID': review.address_id,
            'Address': {
                'id': review.address.id,
                'Door Number': review.address.door_num,
                'Street': review.address.street,
                'Postode': review.address.postcode,
            },
        }
        neighbour_results.append(result)
    data: Dict = {
        'Status': ok_message()[3],
        'Search by neighbour': ok_message()[2],
        'Reviews by neighbours': neighbour_results,   
    }
    return jsonify(data)



# display reviews by visitor API
@app.route('/api/vistors')
def filter_vistor_api() -> Dict:
    session: SessionLocal = SessionLocal()
    check_vistor: Reviews = session.query(Reviews).filter_by(type='vistor').first()
    if check_vistor is None:
        void: Dict = {
            'Search review by visitor': error_message()[1],
            'Status': error_message()[2],
        }
        return jsonify(void)
    all_reviews: List[Reviews] = session.query(Reviews).filter_by(type='visitor').all()
    visitor_result: List[Dict] = []
    for review in all_reviews:
        result = {
            'id': review.id,
            'Rating': review.rating,
            'Review': review.review,
            'Type': review.type,
            'Date': review.date,
            'Address ID': review.address_id,
            'Address': {
                'id': review.address.id,
                'Door Number': review.address.door_num,
                'Street': review.address.street,
                'Postode': review.address.postcode,
            },
        }
        visitor_result.append(result)
    data: Dict = {
        'Status': ok_message()[3],
        'Search by visitors': ok_message()[2],
        'Reviews by vistors': visitor_result, 
    }
    return jsonify(data)


# display reviews by location API
@app.route('/api/location/<location>')
def filter_location_api(location: str) -> Dict:
    session: SessionLocal = SessionLocal()
    check_location: bool = validate_location_request(location)
    if check_location is False:
        void: Dict = {
            'Search review by location': error_message()[1],
            'Status': error_message()[2],
        }
        return jsonify(void)
    user_location_result: List[Dict] = []
    get_reviews: List[Reviews] = session.query(Reviews).all()
    for review in get_reviews:
        if location == review.address.location:
            result = {
                'id': review.id,
                'Rating': review.rating,
                'Review': review.review,
                'Type': review.type,
                'Date': review.date,
                'Address ID': review.address_id,
                'Address': {
                    'id': review.address.id,
                    'Door Number': review.address.street,
                    'Street': review.address.street,
                    'Postode': review.address.postcode,
                },
            }
            user_location_result.append(result)
    data: Dict = {
        'Status': ok_message()[3],
        'Search by loction': ok_message()[2],
        'Reviews by location': user_location_result,
    }
    return jsonify(data)

@app.route('/debug')
def debug():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return '\n'.join(routes)


# add new address API
@app.route('/api/new/address/<address_door>,<address_street>,<address_location>,<address_postcode>')
def create_new_address_api(
    address_door, address_street, address_location, address_postcode
) -> Dict:
    session: SessionLocal = SessionLocal()
    door: str = address_door
    street_name: str = address_street
    town_or_city: str = address_location
    postcode: str = address_postcode

    # check if address already exists via the door number & postcode
    get_door_num: List[Address] = session.query(Address).filter_by(door_num=door).all()
    get_postcode: List[Address] = session.query(Address).filter_by(postcode=postcode).all()
    
    # get coordinates from postcode
    user_postcode_cordinates: List[Dict] = get_postcode_coordinates(postcode)

    # if the list is empty then the new address does NOT already exist
    if len(get_postcode) == 0:
        new_address: Address = Address(
            door_num=door.lower(),
            street=street_name.lower(),
            location=town_or_city.lower(),
            postcode=postcode.lower(),
        )
        session.add(new_address)
        session.commit()

        # if no coordinates found
        if user_postcode_cordinates is None:
            warning: Dict = {
                'Incomplete upload': warning_message()[0],
                'Status': warning_message()[1]
            }
            return jsonify(warning)
        # if coordinates found from postcode
        elif user_postcode_cordinates != None:
            success: Dict = {
                'Successful upload': ok_message()[0],
                'Status': ok_message()[2],
            }
            return jsonify(success)
    # if there is an existing postcode
    else:
        # if the door number does not match
        if not get_door_num and postcode == get_postcode[0].postcode:
            new_address: Address = Address(
                door_num=door.lower(),
                street=street_name.lower(),
                location=town_or_city.lower(),
                postcode=postcode.lower(),
            )
            session.add(new_address)
            session.commit()
           
            if user_postcode_cordinates != None:
                success = {
                    'Add new address': ok_message()[0]['Success'],
                    'Status': ok_message()[3]
                }
                return jsonify(success)
        else:
            # if the address already exists 
            if door == get_door_num[0].door_num and postcode == get_postcode[0].postcode:
                message: str = 'This address is already in the system.'
                void: str = 'Error'
                data: Dict = {void:message}
                return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)