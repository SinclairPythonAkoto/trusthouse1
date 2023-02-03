import requests
from typing import List, Dict, Tuple
from trusthouse import app
from .extensions import SessionLocal
from trusthouse.models import *
from datetime import datetime



def create_new_address(door, street, location, postcode) -> Address:
    """
    Creates a new address entry, storing it in the Address table

    Resturns the Address object after saving it.
    """
    with app.app_context():
        session: SessionLocal = SessionLocal()
        new_address_entry: Address = Address(
                    door_num=door.lower(),
                    street=street.lower(),
                    location=location.lower(),
                    postcode=postcode.lower(),
                )
        session.add(new_address_entry)
        session.commit()
    return new_address_entry



def create_new_buisness(buisness_name, buisness_category, contact_details, address) -> Business:
    """
    Creates a new buisness entry, storing it in the Buisness table.
    Each new entry is linked to the Address id and Maps id.

    Returns the Buisness object back to the user.
    """
    with app.app_context():
        session: SessionLocal = SessionLocal()
        new_buisness_entry: Business = Business(
            name=buisness_name.lower(),
            category=buisness_category.lower(),
            contact=contact_details.lower(),
            place=address,
        )
        session.add(new_buisness_entry)
        session.commit()
    return new_buisness_entry



def new_incident(category, description, address) -> Incident:
    """
    Creates a new incident entry, saving it into the Incident table.
    Each entry is linked to both Address & Maps tables.

    Returns the Incident object back to the user.
    """
    with app.app_context():
        session: SessionLocal = SessionLocal()
        new_incident_entry: Incident = Incident(
            category=category.lower(),
            description=description.lower(),
            date=datetime.now(),
            area=address,
        )
        session.add(new_incident_entry)
        session.commit()
    return new_incident_entry



def create_new_map(longitude, latitude, address) -> Maps:
    """
    Creates a new map entry, storing it in the Maps table.
    The coordinates derived from the user postcode request.
    Each entry is linked to the Address id.
    Returns the Maps object after saving it.
    """
    with app.app_context():
        session: SessionLocal = SessionLocal()
        new_map_entry: Maps = Maps(
            lon=longitude,
            lat=latitude,
            location=address,
        )
        session.add(new_map_entry)
        session.commit()
    return new_map_entry



def create_new_review(rating, review, review_type, address) -> Reviews:
    """
    Creates a new review entry, storing it in the Review table.
    Each review is linked to the Address id.
    Returns the Reviews object after saving it.
    """
    with app.app_context():
        session: SessionLocal = SessionLocal()
        new_review_entry: Reviews = Reviews(
            rating=rating,
            review=review,
            type=review_type,
            date=datetime.now(),
            address=address,
        )
        session.add(new_review_entry)
        session.commit()
    return new_review_entry



def get_postcode_coordinates(postcode) -> List[Dict]:
    """
    Takes the user's postcode request and uses the OpenStreetMap API to get the latitude * longitude.
    Returns a JSON object or empyty list if there is no match from the response.
    """
    BASE_URL: str = 'https://nominatim.openstreetmap.org/search?format=json'

    response: requests = requests.get(f"{BASE_URL}&postalcode={postcode}&country=united kingdom")
    data: List[Dict] = response.json()
    return data



def warning_message() -> Tuple(Dict):
    """
    Returns a warning message if not the longitude & latitude has not been saved into the Maps table.
    Used for backend API and for user front end.
    For backend API reference both tuple indexes.
    For front end warning messages we only need to use the first tuple index : warning_message()[0]['Warning']

    warning_message( )[1] = {'status': 199}
    warning_message( )[1] = 200

    warning_message( )[0] = warning message 
    warning_message( )[1] = status code
    
    Returns a tuple of dictionaries with the warning message and status.
    """
    warning: Dict = {
        'Warning': 'Your address has been uploaded to Trust House, but the coordinates to your postcode could not be saved.'
    }
    status: Dict = {'status': 199}
    return warning, status



def error_message() -> Tuple(Dict):
    """
    Returns an error message if unable to get the request.
    Used for backend API and for user front end messages.
    For backend API reference both tuple indexes.
    For front end error messages we only need to use the first tuple index : error_message()[0]['Error']

    error_message( )[2] = {'status': 400}
    error_message( )[2] = 400

    error_message( )[0] = error message 
    error_message( )[1] = no match found
    error_message( )[2] = status code
    error_message( )[3] = business error
    error_message( )[4] = incident error

    Returns a tuple of dictionaries with the error message and status.
    """
    error: Dict = {
        'Error': 'Could not make your request. Please check and try again.'
    }
    no_match: Dict = {'Error': 'No match found. Please check and try again.'}
    status: Dict = {'status': 400}
    business_error: Dict = {'Error': 'Your listing could not be uploaded. We could not locate the co-ordinates of the postcode given.'}
    incident_error: Dict = {'Error': 'Your incident could not be uploaded. We could not locat ethe co-ordinates of the postcode.'}
    return error, no_match, status, business_error, incident_error



def ok_message() -> Tuple(Dict):
    """
    Returns a message to let the user the request went through.
    Used for backend API and front end messages.
    For backend API reference both tuple indexes.
    For front end OK messages we only need to use the first tuple index : ok_message()[0]['Success']

    ok_message( )[2] = {'status': 200}
    ok_message( )[2] = 200

    ok_message( )[0] = good address & map details
    ok_message( )[1] = good review
    ok_message( )[2] = match found
    ok_message( )[3] = status code
    ok_message( )[4] = good business upload

    returns a tuple of dictionaries with OK messages and the status.
    """
    good_address: Dict = {
        'Success': 'Your address has been uploaded to Trust House.'
    }
    good_review: Dict = {
        'Success': 'Your review has been successfully uploaded to Trust House.'
    }
    match_found: Dict = {'Success': 'A match was found!'}
    status = {'status': 201}
    good_buisness: Dict = {'Success': 'Your business has been successfully uploaded to Trust House.'}
    return good_address, good_review, match_found, status, good_buisness



def validate_business_name(business_name) -> bool:
    '''
    Check if the buisness name exists in the Buisness table.
    Return a boolean object.
    '''
    session: SessionLocal = SessionLocal()
    response: Business = session.query(
            session.query(Business).filter_by(name=business_name).exists()
        ).scalar()
    return response



def validate_door_request(door) -> bool:
    """
    Checks if the postcode exists within the Address table.
    Returns a boolean object.
    """
    session: SessionLocal = SessionLocal()
    response: Address = session.query(
            session.query(Address).filter_by(door_num=door).exists()
        ).scalar()
    return response



def validate_location_request(location) -> bool:
    """
    Checks if the location exists in the Address table.
    Returns a boolean object
    """
    session: SessionLocal = SessionLocal()
    response: Address = session.query(
            session.query(Address).filter_by(location=location).exists()
        ).scalar()
    return response



def validate_postcode_request(postcode) -> bool:
    """
    Checks if the postcode exists within the Addres table.
    Returns a boolean object.
    """
    session: SessionLocal = SessionLocal()
    response: Address = session.query(
            session.query(Address).filter_by(postcode=postcode).exists()
        ).scalar()
    return response



def validate_rating_request(rating) -> bool:
    """
    Checks if the user rating already exists wihtin the Review table.
    Return a boolean object.
    """
    session: SessionLocal = SessionLocal()
    response: Reviews = session.query(
            session.query(Reviews).filter_by(rating=rating).exists()
        ).scalar()
    return response



def validate_review_content(review_content) -> bool:
    """
    Checks if the user review content already exists wihtin the Review table.
    Return a boolean object.
    """
    session: SessionLocal = SessionLocal()
    response: Reviews = session.query(
            session.query(Reviews).filter_by(review=review_content).exists()
        ).scalar()
    return response



def validate_street_request(street) -> bool:
    """
    Checks if the street name already exists in the Address table.
    Returns a boolean object.
    """
    session: SessionLocal = SessionLocal()
    response: Address = session.query(
            session.query(Address).filter_by(street=street).exists()
        ).scalar()
    return response