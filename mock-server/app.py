from flask import Flask, jsonify, request
import json
import os
# Author: Tanuj Kumar  ||  Tanujk95681@gmail.com
# Project: Backend Developer Technical Assessment
# Description: Flask → FastAPI → PostgreSQL data pipeline
app = Flask(__name__)

# Load data from JSON
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')

with open(DATA_FILE) as f:
    customers = json.load(f)


# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})


# Get all customers (with pagination)
@app.route('/api/customers', methods=['GET'])
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    start = (page - 1) * limit
    end = start + limit

    paginated_data = customers[start:end]

    return jsonify({
        "data": paginated_data,
        "total": len(customers),
        "page": page,
        "limit": limit
    })


# Get single customer
@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return jsonify(customer)

    return jsonify({"error": "Customer not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)