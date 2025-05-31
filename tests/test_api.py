import pytest
import json
from app.api import api_blueprint
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_expenses(client):
    resp = client.get('/api/expenses')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)

def test_create_expense(client):
    new_expense = {"name": "Test Expense", "amount": 123.45}
    resp = client.post('/api/expenses', data=json.dumps(new_expense), content_type='application/json')
    assert resp.status_code == 201
    data = resp.get_json()
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
    resp = client.get('/api/expenses/999999')
    assert resp.status_code == 404
    data = resp.get_json()
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
    resp = client.put('/api/expenses/999999', data=json.dumps(updated_data), content_type='application/json')
    assert resp.status_code == 404

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
    resp = client.delete('/api/expenses/999999')
    assert resp.status_code == 404  # Corrected to expect 404 for not found
    data = resp.get_json()
    assert "message" in data


