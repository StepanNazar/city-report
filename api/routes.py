from flask import request

from api import app


@app.route('/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'GET':
        return [
            {
                "id": 1,
                "authorID": 8,
                "authorName": "John",
                "creationTime": "2025-01-22 22:17",
                "latitude": 45.8548,
                "longitude": 89.6545,
                "title": "Lorem",
            }
        ]
    elif request.method == 'POST':
        return {}, 201  # TODO location header????


@app.route('/posts/<int:post_id>', methods=['GET', 'PATCH', 'DELETE'])
def get_post(post_id):
    if request.method == 'GET':
        return {
            "id": 1,
            "authorID": 8,
            "authorName": "John",
            "creationTime": "2025-01-22 22:17",
            "latitude": 45.8548,
            "longitude": 89.6545,
            "country": "ukraine",
            "state": "if oblast",
            "locality": "if",
            "title": "Lorem",
            "body": "lorem"
        }
    elif request.method == 'PATCH':
        return {}, 204
    elif request.method == 'DELETE':
        return {}, 204


@app.route('/auth/me', methods=['GET'])
def get_current_user():
    return {
        "id": 8,
        "username": "john_doe",
        "email": "john@example.com",
        "password": "password123"
    }


@app.route('/auth/login', methods=['POST'])
def login():
    return {
        "id": 8,
        "username": "john_doe",
        "email": "john@example.com"
    }  # TODO 200 or 201? + add jwt token


@app.route('/auth/register', methods=['POST'])
def register():
    return {
        "id": 8,
        "username": "john_doe",
        "email": "john@example.com"
    }, 201  # TODO add jwt token


@app.route('/auth/password', methods=['PATCH'])
def change_password():
    return {}, 204


@app.route('/auth/password/reset-request', methods=['POST'])
def reset_password_request():
    return {}, 202


@app.route('/auth/password/reset', methods=['POST'])
def reset_password():
    return {}, 204
