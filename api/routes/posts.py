from apiflask import APIBlueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from api.schemas.posts import PostSchema

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
    @posts.doc(security="jwt_access_token", responses={201: "Post created"})
    def post(self):
        """Create a new post. Activated account required."""
        return {}, 501


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
    @posts.doc(
        security="jwt_access_token", responses={403: "Forbidden", 200: "Post updated"}
    )
    def put(self, post_id):
        """Update a post by ID. Only the author can update the post."""
        return {}, 501

    @jwt_required()
    @posts.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "Post partially updated"},
    )
    def patch(self, post_id):
        """Edit a post by ID using JSON Patch. Only the author can edit the post."""
        return {}, 501

    @jwt_required()
    @posts.doc(
        security="jwt_access_token", responses={204: "Post deleted", 403: "Forbidden"}
    )
    def delete(self, post_id):
        """Delete a post by ID. Only the author can delete the post."""
        return {}, 501


class PostReaction(MethodView):
    @jwt_required()
    @posts.doc(security="jwt_access_token", responses={204: "Reaction added/updated"})
    def put(self, post_id):
        """Add or update reaction to the post. Activated account required."""
        return {}, 501

    @jwt_required()
    @posts.doc(security="jwt_access_token", responses={204: "Reaction removed"})
    def delete(self, post_id):
        """Remove reaction from the post. Activated account required."""
        return {}, 501


class PostReport(MethodView):
    @jwt_required()
    @posts.doc(security="jwt_access_token", responses={201: "Report created"})
    def post(self, post_id):
        """Report post. Activated account required."""
        return {}, 501


class PostComments(MethodView):
    def get(self, post_id):
        """Get comments for post"""
        return {}, 501

    @jwt_required()
    @posts.doc(security="jwt_access_token", responses={201: "Comment created"})
    def post(self, post_id):
        """Create a new comment for the post. Activated account required."""
        return {}, 501


class PostSolutions(MethodView):
    def get(self, post_id):
        """Get solutions for post"""
        return {}, 501

    @jwt_required()
    @posts.doc(security="jwt_access_token", responses={201: "Solution created"})
    def post(self, post_id):
        """Create a new solution for post. Activated account required."""
        return {}, 501


posts.add_url_rule("/posts", view_func=Posts.as_view("posts"))
posts.add_url_rule("/posts/<int:post_id>", view_func=Post.as_view("post"))
posts.add_url_rule(
    "/posts/<int:post_id>/reaction", view_func=PostReaction.as_view("post_reaction")
)

posts.add_url_rule(
    "/posts/<int:post_id>/report", view_func=PostReport.as_view("post_report")
)
posts.add_url_rule(
    "/posts/<int:post_id>/comments", view_func=PostComments.as_view("post_comments")
)
posts.add_url_rule(
    "/posts/<int:post_id>/solutions", view_func=PostSolutions.as_view("post_solutions")
)
