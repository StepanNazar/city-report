from flask.views import MethodView
from flask_jwt_extended import jwt_required

from api.blueprints.comments import comments
from api.blueprints.comments.schemas import (
    CommentOutPaginationSchema,
    CommentOutSchema,
    CommentSortingSchema,
)
from api.blueprints.common.schemas import (
    TextBodySchema,
    merge_schemas,
    pagination_query_schema,
)
from api.blueprints.users.schemas import ReactionSchema


class Comment(MethodView):
    @comments.output(CommentOutSchema)
    def get(self, comment_id):
        """Get comment by ID"""
        return {}, 501

    @jwt_required()
    @comments.input(TextBodySchema)
    @comments.output(CommentOutSchema)
    @comments.doc(
        security="jwt_access_token",
        responses={200: "Comment updated", 403: "Forbidden"},
    )
    def put(self, comment_id):
        """Update comment. Only the comment author can update it."""
        return {}, 501

    @jwt_required()
    @comments.doc(
        security="jwt_access_token",
        responses={204: "Comment deleted", 403: "Forbidden"},
    )
    def delete(self, comment_id):
        """Delete comment. Only the comment author can delete it."""
        return {}, 501


class CommentReaction(MethodView):
    @jwt_required()
    @comments.input(ReactionSchema)
    @comments.doc(
        security="jwt_access_token", responses={204: "Reaction added/updated"}
    )
    def put(self, comment_id):
        """Put reaction to comment. Activated account required."""
        return {}, 501

    @jwt_required()
    @comments.doc(security="jwt_access_token", responses={204: "Reaction removed"})
    def delete(self, comment_id):
        """Remove reaction from comment. Activated account required."""
        return {}, 501


class CommentReport(MethodView):
    @jwt_required()
    @comments.input(TextBodySchema)
    @comments.doc(security="jwt_access_token", responses={204: "Report created"})
    def post(self, comment_id):
        """Report comment. Activated account required."""
        return {}, 501


class CommentReplies(MethodView):
    @comments.input(
        merge_schemas(pagination_query_schema(), CommentSortingSchema), location="query"
    )
    @comments.output(CommentOutPaginationSchema)
    def get(self, comment_id, query_data):
        """Get replies to a comment"""
        return {}, 501

    @jwt_required()
    @comments.input(TextBodySchema)
    @comments.output(CommentOutSchema, status_code=201)
    @comments.doc(security="jwt_access_token", responses={201: "Reply created"})
    def post(self, comment_id):
        """Create a new reply to a comment. Activated account required."""
        return {}, 501


comments.add_url_rule(
    "/comments/<int:comment_id>", view_func=Comment.as_view("comment")
)
comments.add_url_rule(
    "/comments/<int:comment_id>/reaction",
    view_func=CommentReaction.as_view("comment_reaction"),
)
comments.add_url_rule(
    "/comments/<int:comment_id>/report",
    view_func=CommentReport.as_view("comment_report"),
)
comments.add_url_rule(
    "/comments/<int:comment_id>/replies",
    view_func=CommentReplies.as_view("comment_replies"),
)
