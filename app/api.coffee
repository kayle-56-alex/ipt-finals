
from flask import Blueprint, request, jsonify
from app import db
from models import Expense

api = Blueprint('api', __name__, url_prefix='/api')

# Get all expenses
@api.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([e.to_dict() for e in expenses])

# Get one expense by ID
@api.route('/expenses/<int:id>', methods=['GET'])
def get_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    return jsonify(expense.to_dict())

# Create new expense
@api.route('/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()
    if not data or not all(k in data for k in ['amount', 'category', 'date']):
        return jsonify({'error': 'Missing required fields'}), 400
    expense = Expense(amount=data['amount'], category=data['category'], date=data['date'])
    db.session.add(expense)
    db.session.commit()
    return jsonify(expense.to_dict()), 201

# Update expense
@api.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    data = request.get_json()
    if 'amount' in data:
        expense.amount = data['amount']
    if 'category' in data:
        expense.category = data['category']
    if 'date' in data:
        expense.date = data['date']
    db.session.commit()
    return jsonify(expense.to_dict())

# Delete expense
@api.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted'})
