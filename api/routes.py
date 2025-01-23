import requests
from flask import request, jsonify

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
        return {}, 201  # location header????


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


# com struct {
# comId
# postID
# who create
# body
# countof likes dislikes
# }
@app.route('/comentsForId', methods=['GET'])
def get_coments_by_id():
    com_id = request.args.get('id', type=int, default=0)  # Отримуємо параметр id
    if com_id <= 0:
        return jsonify({"error": "Invalid ID"}), 400  # Перевірка на валідність id

    # Формуємо URL для отримання коментарів
    url = f"https://jsonplaceholder.typicode.com/posts/{com_id}/comments"

    try:
        # Виконуємо GET-запит до JSONPlaceholder
        response = requests.get(url)
        response.raise_for_status()  # Перевіряємо статус відповіді (404, 500 тощо)

        # Повертаємо отримані дані у вигляді JSON
        return jsonify(response.json())
    except:
        return jsonify({"error": "Failed to fetch comments"}), 500


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
    }  # 200 or 201? + add jwt token


@app.route('/auth/register', methods=['POST'])
def register():
    return {
        "id": 8,
        "username": "john_doe",
        "email": "john@example.com"
    }, 201  # add jwt token


@app.route('/auth/password', methods=['PATCH'])
def change_password():
    return {}, 204


@app.route('/auth/password/reset-request', methods=['POST'])
def reset_password_request():
    return {}, 202


@app.route('/auth/password/reset', methods=['POST'])
def reset_password():
    return {}, 204
