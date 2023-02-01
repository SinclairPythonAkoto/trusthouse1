import os
from trusthouse import app
from trusthouse.extensions import init_db, SessionLocal
from trusthouse.models import Address
from trusthouse.utils import ok_message, error_message
from flask import jsonify
from dotenv import load_dotenv
load_dotenv()

init_db()

# Configure the app with the db object
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TRUSTHOUSE_DB']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# config your host & port for app using environment variable
HOST = os.environ['HOST']
PORT = os.environ['API_PORT']


# create api routes

# instructions / manual
@app.route('/')
def api_home():
    manual = {
        'APP': 'TrustHouse API',
        'DESCRIPTION': 'This will be the manual or instructions on how to use the API.',
        'STATUS': ok_message()[3]
    }
    return jsonify(manual)

# display all address API
@app.route('/api/display/addresses')
def display_address_api():
    session = SessionLocal()
    check_address = session.query(Address).first()
    if check_address is None:
        return jsonify(error_message()[1])
    all_addresses = session.query(Address).all()
    db_query_result = []
    for address in all_addresses:
        result = {
                'id': address.id,
                'Door Number': address.door_num,
                'Street Name': address.street,
                'Location': address.location,
                'Postcode': address.postcode,
        }
        db_query_result.append(result)
    data = {
            'Search all addresses': ok_message()[2],
            'Display Addresses': db_query_result,
            'Status': ok_message()[3],
        }
    return jsonify(data)





if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)