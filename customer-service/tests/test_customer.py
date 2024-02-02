# import pytest
# import responses
# from flask import Flask
# from customer import internal_routes  # replace with the name of your Flask app
# 
# app = Flask(__name__)
# app.register_blueprint(internal_routes)
# 
# 
# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client
# 
# 
# @responses.activate
# def test_add_customer(client):
#     responses.add(responses.POST, '/internal_customer',
#                   json={'status': {'code': 201, 'message': 'Success, Customer created successfully!'}}, status=201)
#     response = client.post('/internal_customer', json={'name': 'test', 'email': 'test@test.com', 'password': 'test'})
#     assert response.status_code == 201
#     assert response.get_json()['status']['message'] == 'Success, Customer created successfully!'
# 
# 
# @responses.activate
# def test_add_existing_customer(client):
#     responses.add(responses.POST, '/internal_customer',
#                   json={'status': {'code': 400, 'message': 'Customer already exists'}}, status=400)
#     response = client.post('/internal_customer', json={'name': 'test', 'email': 'test@test.com', 'password': 'test'})
#     assert response.status_code == 400
#     assert response.get_json()['status']['message'] == 'Customer already exists'
# 
# 
# ========================================================================================
# 
# import pytest
# from unittest.mock import patch, MagicMock
# from flask import Flask
# from models.models import Customer, Certificate
# from customer import internal_routes  # replace with the name of your Flask app
# 
# app = Flask(__name__)
# app.register_blueprint(internal_routes)
# 
# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         with app.app_context():
#             yield client
# 
# @patch('models.models.Customer.query')
# def test_add_customer(mock_query, client):
#     mock_query.filter_by.return_value.first.return_value = None
#     response = client.post('/internal_customer', json={'name': 'test', 'email': 'test@test.com', 'password': 'test'})
#     assert response.status_code == 201
#     assert response.get_json()['status']['message'] == 'Success, Customer created successfully!'
# 
# @patch('models.models.Customer.query')
# def test_add_existing_customer(mock_query, client):
#     mock_query.filter_by.return_value.first.return_value = Customer()
#     response = client.post('/internal_customer', json={'name': 'test', 'email': 'test@test.com', 'password': 'test'})
#     assert response.status_code == 400
#     assert response.get_json()['status']['message'] == 'Customer already exists'
# 
# @patch('models.models.Customer.query')
# def test_delete_nonexistent_customer(mock_query, client):
#     mock_query.get.return_value = None
#     response = client.delete('/internal_customer/1')
#     assert response.status_code == 404
#     assert response.get_json()['status']['message'] == 'Customer does not exist'
