"""

request_ handler validates the schema of incoming requests and routes then to their appropriate services


"""


from flask import Blueprint
from flask import request
import requests
from common_packages.constants.constants import USER_SCHEMA, CERT_SCHEMA, CERT_STATUS_SCHEMA
from common_packages.utils.schema_valiadator import validate_schema
from logs.logging_config import setup_logger

routes = Blueprint('routes', __name__)

log = setup_logger(__file__)


@routes.route('/', methods=['GET'])
def hello():
    log.info("GET request received at '/' endpoint")
    return "Hello"


@routes.route('/v1/customer', methods=['POST'])
def create_user():
    data = request.get_json()
    if validate_schema(data, USER_SCHEMA):
        response = requests.post('http://customer-service:8000/internal_customer', json=data)
        log.info(f"Received request to create customer with:{data}")
        # Return the response received from the second service
        return response.content, response.status_code


@routes.route('/v1/customer/<customer_id>', methods=['DELETE'])
def delete_user(customer_id):
    response = requests.delete(f'http://customer-service:8000/internal_customer/{customer_id}')
    log.info(f"Received request to delete customer with id :{customer_id}")
    # Return the response received from the second service
    return response.content, response.status_code


@routes.route('/v1/certificate', methods=['POST'])
def create_certificate():
    data = request.get_json()
    if validate_schema(data, CERT_SCHEMA):
        response = requests.post('http://cert-service:5001/internal-certificate', json=data)
        log.info(f"Received request to create certificate with:{data}")
        # Return the response received from the second service
        return response.content, response.status_code


@routes.route('/v1/certificates/<customer_id>', methods=['GET'])
def get_active_certificates(customer_id):
    response = requests.get(f'http://cert-service:5001/internal-certificates/{customer_id}')
    log.info(f"Received request to get all active certificates for  customer {customer_id}")
    # Return the response received from the second service
    return response.content, response.status_code


@routes.route('/v1/certificate/<certificate_id>', methods=['PATCH'])
def change_certificate_status(certificate_id):
    data = request.get_json()
    if validate_schema(data, CERT_STATUS_SCHEMA):
        response = requests.patch(f'http://cert-service:5001/internal-certificate/{certificate_id}', json=data)
        log.info(f"Received request to update certificate status for certificate:{certificate_id}")
        # Return the response received from the second service
        return response.content, response.status_code


