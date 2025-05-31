from flask import Blueprint, jsonify, request

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

expenses = [
    {"id": 1, "name": "Groceries", "amount": 50.0},
    {"id": 2, "name": "Electricity Bill", "amount": 75.25},
]

@api_blueprint.route('/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses), 200

@api_blueprint.route('/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()
    if not data or 'name' not in data or 'amount' not in data:
        return jsonify({"message": "Missing 'name' or 'amount' in request"}), 400
    
    new_id = max(exp['id'] for exp in expenses) + 1 if expenses else 1
    new_expense = {
        "id": new_id,
        "name": data['name'],
        "amount": data['amount']
    }
    expenses.append(new_expense)
    return jsonify(new_expense), 201

@api_blueprint.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    expense = next((exp for exp in expenses if exp["id"] == expense_id), None)
    if expense:
        return jsonify(expense), 200
    return jsonify({"message": "Expense not found"}), 404

@api_blueprint.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = next((exp for exp in expenses if exp["id"] == expense_id), None)
    if not expense:
        return jsonify({"message": "Expense not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing JSON data"}), 400

    expense['name'] = data.get('name', expense['name'])
    expense['amount'] = data.get('amount', expense['amount'])
    return jsonify(expense), 200

@api_blueprint.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    global expenses
    expense_exists = any(exp["id"] == expense_id for exp in expenses)
    if not expense_exists:
        return jsonify({"message": "Expense not found"}), 404

    expenses = [exp for exp in expenses if exp["id"] != expense_id]
    return jsonify({"message": "Expense deleted"}), 200


