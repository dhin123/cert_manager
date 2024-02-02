from flask import request, jsonify, Blueprint
from models.models import Customer, Certificate, db
from sqlalchemy.exc import SQLAlchemyError
import random
from utils.id_generator import SnowflakeIdGenerator
from werkzeug.security import generate_password_hash
from logs.logging_config import setup_logger

log = setup_logger(__file__)

internal_routes = Blueprint('internal_routes', __name__)


@internal_routes.route('/get_api', methods=['GET'])
def say_hello():
    return "Hello from cert manager"


@internal_routes.route('/internal_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    log.info(f"Received request to create customer with:{data}")
    id_generator = SnowflakeIdGenerator(worker_id=random.randint(0, 4), datacenter_id=random.randint(0, 4))
    
    # generate_password_hash method takes care of hashing and salting
    password_hash = generate_password_hash(data['password'])
    new_customer = Customer(id=id_generator.generate(), name=data['name'], email=data['email'],
                            password=password_hash)
    existing_customer = Customer.query.filter_by(email=data['email']).first()
    customer_id = new_customer.to_dict()['id']
    if existing_customer is None:
        try:
            db.session.add(new_customer)
            db.session.commit()
            log.info(f"Successfully created Customer with id: {customer_id}")
            return jsonify(
                {
                    "status":
                        {
                            "code": 201,
                            "message": "Customer created successfully!",
                            "customer_id": customer_id
                        }
                }), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            log.info(f"Error occurred while creating customer: {str(e)}")
            return jsonify({
                "status": {
                    "code": 500,
                    "message": "Internal Server error",
                    "error": str(e),

                }
            }), 500
    else:
        log.info(f"Attempted to create a customer that already exists: {data['email']}")
        return jsonify({
            "status": {
                "code": 400,
                "message": "Customer already exists",

            }
        }), 400


@internal_routes.route('/internal_customer/<customer_id>', methods=['DELETE'])
def delete_user(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        log.info(f"Attempted to delete a customer that does not exist: {customer_id}")
        return jsonify({
            "status": {
                "code": 404,
                "message": "Customer does not exist"
            }
        }), 404
    certs = Certificate.query.filter_by(customer_id=customer_id).first()
    # deletes the customer only when customer is not associated with any certificate irrespective of the cert status
    if certs is not None:
        log.info(f"Attempted to delete a customer associated with one or more certificates")
        return jsonify(
            {
                "status": {
                    "code": 400,
                    "message": "Delete unsuccessful. Customer is associated with one or more certificates."
                }
            }
        ), 400

    try:
        db.session.delete(customer)
        db.session.commit()
        log.info(f"Successfully deleted customer with id: {customer_id}")
        return jsonify({
            "status": {
                "code": 200,
                "message": "Customer deleted successfully!"
            }
        }), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        log.info(f"Error occurred while deleting customer: {str(e)}")
        return jsonify({
            "status": {
                "code": 500,
                "message": "Internal server error"
            }
        }), 500


