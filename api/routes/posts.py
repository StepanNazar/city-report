import requests
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace

# later path can be changed, but kept as / for now to match the frontend
posts = Namespace('posts', description='Posts operations', path='/')


@posts.route('/posts')
class Posts(Resource):
    def get(self):
        """Get all posts"""
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

    @jwt_required()
    def post(self):
        """Create a new post"""
        return {}, 201


@posts.route('/posts/<int:post_id>')
class Post(Resource):
    def get(self, post_id):
        """Get a post by ID"""
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

    @jwt_required()
    def patch(self, post_id):
        """Edit a post by ID"""
        return {}, 204

    @jwt_required()
    def delete(self, post_id):
        """Delete a post by ID"""
        return {}, 204


# com struct {
# comId
# postID
# who create
# body
# countof likes dislikes
# }
@posts.route('/comentsForId')
class ComentsForId(Resource):
    def get(self):
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
