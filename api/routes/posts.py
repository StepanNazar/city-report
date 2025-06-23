import requests
from apiflask import APIBlueprint
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from api.schemas.posts import PostSchema

# later path can be changed, but kept as / for now to match the frontend
posts = APIBlueprint("posts", __name__, tag="Posts operations", url_prefix="/")


class Posts(MethodView):
    @posts.output(PostSchema(many=True))
    def get(self):
        """Get all posts"""
        return {}, 501
        # return [
        #     {
        #         "id": 1,
        #         "authorID": 8,
        #         "authorName": "John",
        #         "creationTime": "2025-01-22 22:17",
        #         "latitude": 45.8548,
        #         "longitude": 89.6545,
        #         "title": "Lorem",
        #     }
        # ]

    @jwt_required()
    def post(self):
        """Create a new post"""
        return {}, 201


class Post(MethodView):
    @posts.output(PostSchema)
    def get(self, post_id):
        """Get a post by ID"""
        return {}, 501
        # return {
        #     "id": 1,
        #     "authorID": 8,
        #     "authorName": "John",
        #     "creationTime": "2025-01-22 22:17",
        #     "latitude": 45.8548,
        #     "longitude": 89.6545,
        #     "country": "ukraine",
        #     "state": "if oblast",
        #     "locality": "if",
        #     "title": "Lorem",
        #     "body": "lorem",
        # }

    @jwt_required()
    @posts.input(PostSchema(partial=True))
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
class ComentsForId(MethodView):
    def get(self):
        com_id = request.args.get("id", type=int, default=0)  # Отримуємо параметр id
        if com_id <= 0:
            return jsonify({"error": "Invalid ID"}), 400  # Перевірка на валідність id

        # Формуємо URL для отримання коментарів
        url = f"https://jsonplaceholder.typicode.com/posts/{com_id}/comments"

        try:
            # Виконуємо GET-запит до JSONPlaceholder
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Перевіряємо статус відповіді (404, 500 тощо)

            # Повертаємо отримані дані у вигляді JSON  # noqa # у is Cyrillic
            return jsonify(response.json())
        except requests.RequestException:
            return jsonify({"error": "Failed to fetch comments"}), 500


posts.add_url_rule("/posts", view_func=Posts.as_view("all_posts"))
posts.add_url_rule("/posts/<int:post_id>", view_func=Post.as_view("specific_post"))
posts.add_url_rule("/comentsForId", view_func=ComentsForId.as_view("coments_for_id"))
