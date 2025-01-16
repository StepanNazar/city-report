from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Список користувачів
users = []

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if 'name' in data and 'description' in data:
        new_user = {
            'name': data['name'],
            'description': data['description']
        }
        users.append(new_user)
        return jsonify({'message': 'User added successfully!'}), 200
    return jsonify({'error': 'Name and description are required!'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
