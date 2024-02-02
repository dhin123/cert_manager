import pytest
from unittest.mock import patch
from flask import Flask
from models.models import Customer
from customer import internal_routes
import responses

app = Flask(__name__)
app.register_blueprint(internal_routes)


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


@responses.activate
@patch('models.models.db.session')
@patch('models.models.Customer.query')
def test_add_customer(mocked_query, mocked_db, client):
    # Mock the SQLAlchemy session add and commit methods
    mocked_db.add.return_value = None
    mocked_db.commit.return_value = None

    # Mock the query to return None, indicating no existing customer
    mocked_query.filter_by.return_value.first.return_value = None

    responses.add(responses.POST, '/internal_customer',
                  json={'status': {'code': 201, 'message': 'Customer created successfully!'}}, status=201)
    response = client.post('/internal_customer', json={'name': 'test', 'email': 'test@test.com', 'password': 'test'})
    assert response.status_code == 201
    assert response.get_json()['status']['message'] == "Customer created successfully!"
    assert 'customer_id' in response.get_json()['status']
    assert response.get_json()['status']['customer_id'] is not None


@patch('models.models.Customer.query')
def test_add_existing_customer(mock_query, client):
    mock_query.filter_by.return_value.first.return_value = Customer()
    response = client.post('/internal_customer', json={'name': 'test', 'email': 'test@test.com', 'password': 'test'})
    assert response.status_code == 400
    assert response.get_json()['status']['message'] == 'Customer already exists'


@patch('models.models.Customer.query')
def test_delete_nonexistent_customer(mock_query, client):
    mock_query.get.return_value = None
    response = client.delete('/internal_customer/1')
    assert response.status_code == 404
    assert response.get_json()['status']['message'] == 'Customer does not exist'
