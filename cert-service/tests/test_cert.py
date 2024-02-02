from unittest.mock import patch, MagicMock
import pytest
from flask import Flask
from models.models import Certificate, Customer
from certificate import cert_routes

app = Flask(__name__)
app.register_blueprint(cert_routes)


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


@patch('certificate.SnowflakeIdGenerator')
@patch('certificate.generate_private_key_and_cert_body')
@patch('models.models.Customer.query')
def test_create_certificate(mock_query, mock_generate, mock_snowflake, client):
    mock_query.get.return_value = Customer()
    mock_generate.return_value = ('private_key', 'certificate_body')
    mock_snowflake.return_value.generate.return_value = '12345'
    response = client.post('/internal-certificate', json={'customer_id': '1'})
    assert response.status_code == 201
    assert response.get_json()['status']['message'] == 'Success,Certificate created successfully!'
    assert response.get_json()['status']['certificate_id'] == '12345'


@patch('models.models.Customer.query')
def test_create_certificate_invalid_customer(mock_query, client):
    mock_query.get.return_value = None
    response = client.post('/internal-certificate', json={'customer_id': '1'})
    assert response.status_code == 404
    assert response.get_json()['status']['message'] == 'Invalid Customer'


@patch('models.models.Certificate.query')
@patch('models.models.Customer.query')
def test_get_active_certificates(mock_customer_query, mock_certificate_query, client):
    mock_customer_query.get.return_value = Customer()
    mock_certificate_query.filter_by.return_value.all.return_value = [Certificate()]
    response = client.get('/internal-certificates/1')
    assert response.status_code == 200
    assert response.get_json()['status']['message'] == 'Success'


@patch('models.models.Certificate.query')
def test_get_active_certificates_invalid_customer(mock_query, client):
    mock_query.get.return_value = None
    response = client.get('/internal-certificates/1')
    assert response.status_code == 404
    assert response.get_json()['status']['message'] == 'Invalid Customer'


@patch('requests.post')
@patch('models.models.Certificate.query')
def test_change_certificate_status(mock_query, mock_post, client):
    mock_query.get.return_value = Certificate()
    mock_post.return_value.status_code = 200
    response = client.patch('/internal-certificate/1', json={'status': 'activate'})
    assert response.status_code == 200
    assert response.get_json()['status']['message'] == 'Certificate Status is changed. Certificate is now Activated'


@patch('models.models.Certificate.query')
def test_change_certificate_status_invalid_certificate(mock_query, client):
    mock_query.get.return_value = None
    response = client.patch('/internal-certificate/1', json={'status': 'activate'})
    assert response.status_code == 404
    assert response.get_json()['status']['message'] == 'Invalid Certificate'

