import requests
from flask import request, jsonify, Blueprint
from models.models import Certificate, Customer, db
from sqlalchemy.exc import SQLAlchemyError
import random
from utils.id_generator import SnowflakeIdGenerator
from utils.private_key_and_body_generator import generate_private_key_and_cert_body
from logs.logging_config import setup_logger

log = setup_logger(__file__)

cert_routes = Blueprint('cert_routes', __name__)


@cert_routes.route('/internal-certificate', methods=['POST'])
def create_certificate():
    data = request.get_json()
    log.info(f"Received request to create certificate with:{data}")
    customer_id = data['customer_id']
    customer = Customer.query.get(customer_id)
    if customer is not None:
        id_generator = SnowflakeIdGenerator(worker_id=random.randint(0, 4), datacenter_id=random.randint(0, 4))
        private_key, certificate_body = generate_private_key_and_cert_body()
        new_certificate = Certificate(id=id_generator.generate(), customer_id=customer_id, active=False,
                                      private_key=private_key,
                                      certificate_body=certificate_body)
        certificate_id = new_certificate.to_dict()['id']
        log.info(f"Created new certificate with id: {certificate_id} for customer: {customer_id}")
    else:
        log.info(f"Invalid customer id: {customer_id}")
        return jsonify({
            "status": {
                "code": 404,
                "message": "Invalid Customer",

            }
        }), 404
    try:
        db.session.add(new_certificate)
        db.session.commit()
        return jsonify({
            "status":
                {
                    "code": 201,
                    "message": "Success,Certificate created successfully!",
                    "certificate_id": certificate_id
                }
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        log.info(f"Error occurred while adding new certificate to the database: {str(e)}")
        return jsonify({
            "status": {
                "code": 400,
                "message": "ERROR",
                "error": str(e)
            }
        }), 400


@cert_routes.route('/internal-certificates/<customer_id>', methods=['GET'])
def get_active_certificates(customer_id):
    customer = Customer.query.get(customer_id)
    log.info(f"Received request to get active certificates for customer with id: {customer_id}")
    if customer is not None:
        # Query for all active certificates for the customer
        active_certificates = Certificate.query.filter_by(customer_id=customer_id, active=True).all()

        # Now `active_certificates` is a list of Certificate instances
        # You can convert them to dict using the `to_dict` method
        active_certificates_dict = [certificate.to_dict() for certificate in active_certificates]

        # Print or return the result
        return jsonify({
            "status": {
                "code": 200,
                "message": "Success",
                "certificates": active_certificates_dict

            }
        }), 200
    else:
        log.info(f"Invalid customer id: {customer_id}")
        return jsonify({
            "status": {
                "code": 404,
                "message": "Invalid Customer",

            }
        }), 404


@cert_routes.route('/internal-certificate/<certificate_id>', methods=['PATCH'])
def change_certificate_status(certificate_id):
    data = request.get_json()
    log.info(f"Received request to change certificate status with data: {data}")
    status = data["status"]
    if status == "activate":
        status_value = True
    else:
        status_value = False
    status_message = "Activated" if status_value else "Deactivated"
    certificate = Certificate.query.get(certificate_id)
    if certificate is not None:
        certificate.active = status_value
        try:
            db.session.commit()
            # call the notification service
            notification_service_url = "http://notification-service:8001/internal-notification"
            response = requests.post(notification_service_url,
                                     json={"certificate_id": certificate_id,
                                           "status": f"Certificate Status is changed. Certificate is now {status_message}"})

            return jsonify({
                "status": {
                    "code": 200,
                    "message": f"Certificate Status is changed. Certificate is now {status_message}",

                }
            }), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            log.info(f"Error changing certificate status: {str(e)}")
            return jsonify({
                "status": {
                    "code": 400,
                    "message": "ERROR",
                    "error": str(e)
                }
            }
            ), 400
    else:
        return jsonify({
            "status": {
                "code": 404,
                "message": "Invalid Certificate",

            }
        }), 404


