import sys
import os
import pytest
import json
from flask import Flask

# Add the root folder to sys.path so 'app' package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api import api_blueprint, expenses

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(api_blueprint)
    return app

@pytest.fixture
def client(app):
    # Reset expenses list before each test to initial state
    expenses.clear()
    expenses.extend([
        {"id": 1, "name": "Groceries", "amount": 50.0},
        {"id": 2, "name": "Electricity Bill", "amount": 75.25},
    ])
    return app.test_client()

def test_get_expenses(client):
    response = client.get('/api/expenses')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_create_expense(client):
    new_expense = {"name": "Test Expense", "amount": 123.45}
    response = client.post('/api/expenses', data=json.dumps(new_expense), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == new_expense["name"]
    assert data["amount"] == new_expense["amount"]
    assert "id" in data

def test_get_expense(client):
    new_expense = {"name": "Get Test", "amount": 10.0}
    post_resp = client.post('/api/expenses', data=json.dumps(new_expense), content_type='application/json')
    expense_id = post_resp.get_json()["id"]

    get_resp = client.get(f'/api/expenses/{expense_id}')
    assert get_resp.status_code == 200
    data = get_resp.get_json()
    assert data["id"] == expense_id
    assert data["name"] == new_expense["name"]

def test_get_expense_not_found(client):
    response = client.get('/api/expenses/999999')
    assert response.status_code == 404
    data = response.get_json()
    assert "message" in data

def test_update_expense(client):
    new_expense = {"name": "Update Test", "amount": 20.0}
    post_resp = client.post('/api/expenses', data=json.dumps(new_expense), content_type='application/json')
    expense_id = post_resp.get_json()["id"]

    updated_data = {"name": "Updated Name", "amount": 30.0}
    put_resp = client.put(f'/api/expenses/{expense_id}', data=json.dumps(updated_data), content_type='application/json')
    assert put_resp.status_code == 200
    data = put_resp.get_json()
    assert data["name"] == updated_data["name"]
    assert data["amount"] == updated_data["amount"]

def test_update_expense_not_found(client):
    updated_data = {"name": "No Expense", "amount": 0}
    response = client.put('/api/expenses/999999', data=json.dumps(updated_data), content_type='application/json')
    assert response.status_code == 404
    data = response.get_json()
    assert "message" in data

def test_delete_expense(client):
    new_expense = {"name": "Delete Test", "amount": 40.0}
    post_resp = client.post('/api/expenses', data=json.dumps(new_expense), content_type='application/json')
    expense_id = post_resp.get_json()["id"]

    del_resp = client.delete(f'/api/expenses/{expense_id}')
    assert del_resp.status_code == 200
    data = del_resp.get_json()
    assert "message" in data

    get_resp = client.get(f'/api/expenses/{expense_id}')
    assert get_resp.status_code == 404

def test_delete_expense_not_found(client):
    response = client.delete('/api/expenses/999999')
    assert response.status_code == 404
    data = response.get_json()
    assert "message" in data



