import datetime

from apiflask import abort
from flask.views import MethodView
from flask_jwt_extended import get_current_user, jwt_required

from api import db
from api.blueprints.comments.schemas import (
    CommentOutPaginationSchema,
    CommentOutSchema,
    CommentSortingSchema,
)
from api.blueprints.common.schemas import (
    JSONPatchSchema,
    TextBodySchema,
    merge_schemas,
    pagination_query_schema,
)
from api.blueprints.solutions import solutions
from api.blueprints.solutions.models import Solution as SolutionModel
from api.blueprints.solutions.schemas import SolutionInSchema, SolutionOutSchema
from api.blueprints.users.schemas import ReactionSchema


class Solution(MethodView):
    @solutions.output(SolutionOutSchema)
    def get(self, solution_id):
        """Get the solution by ID"""
        solution = SolutionModel.query.get_or_404(solution_id, description="Solution not found")
        return solution

    @jwt_required()
    @solutions.input(SolutionInSchema)
    @solutions.output(SolutionOutSchema)
    @solutions.doc(
        security="jwt_access_token",
        responses={200: "Solution updated", 403: "Forbidden"},
    )
    def put(self, solution_id, json_data):
        """Update solution. Only the author of the solution can update it"""
        current_user = get_current_user()
        solution = SolutionModel.query.get_or_404(solution_id, description="Solution not found")

        if solution.author_id != current_user.id:
            abort(403, message="You can only update your own solutions")

        # Update solution fields dynamically
        for key, value in json_data.items():
            if hasattr(solution, key):
                setattr(solution, key, value)

        solution.edited_at = datetime.datetime.now(datetime.UTC)

        db.session.commit()

        return solution

    @jwt_required()
    @solutions.input(JSONPatchSchema)
    @solutions.output(SolutionOutSchema)
    @solutions.doc(
        security="jwt_access_token",
        responses={200: "Solution partially updated", 403: "Forbidden"},
    )
    def patch(self, solution_id):
        """Partially update solution using JSON Patch. Only the author of the solution can edit it."""
        return {}, 501

    @jwt_required()
    @solutions.doc(
        security="jwt_access_token",
        responses={204: "Solution deleted", 403: "Forbidden"},
    )
    def delete(self, solution_id):
        """Delete the solution. Only the author of the solution can delete it."""
        current_user = get_current_user()
        solution = SolutionModel.query.get_or_404(solution_id, description="Solution not found")

        if solution.author_id != current_user.id:
            abort(403, message="You can only delete your own solutions")

        db.session.delete(solution)
        db.session.commit()

        return "", 204


class SolutionApproval(MethodView):
    @jwt_required()
    @solutions.doc(
        security="jwt_access_token",
        responses={204: "Solution approved", 403: "Forbidden"},
    )
    def put(self, solution_id):
        """Approve the solution. Only the author of the post can approve the solution."""
        return {}, 501

    @jwt_required()
    @solutions.doc(
        security="jwt_access_token",
        responses={204: "Solution approval removed", 403: "Forbidden"},
    )
    def delete(self, solution_id):
        """Remove approval of the solution. Only the author of the post can remove approval."""
        return {}, 501


class SolutionReaction(MethodView):
    @jwt_required()
    @solutions.input(ReactionSchema)
    @solutions.doc(
        security="jwt_access_token", responses={204: "Reaction added/updated"}
    )
    def put(self, solution_id):
        """Add or update reaction to the solution. Activated account required."""
        return {}, 501

    @jwt_required()
    @solutions.doc(security="jwt_access_token", responses={204: "Reaction removed"})
    def delete(self, solution_id):
        """Remove reaction from the solution. Activated account required."""
        return {}, 501


class SolutionReport(MethodView):
    @jwt_required()
    @solutions.input(TextBodySchema)
    @solutions.doc(security="jwt_access_token", responses={201: "Report created"})
    def post(self, solution_id):
        """Report solution. Activated account required."""
        return {}, 501


class SolutionComments(MethodView):
    @solutions.input(
        merge_schemas(pagination_query_schema(), CommentSortingSchema), location="query"
    )
    @solutions.output(CommentOutPaginationSchema)
    def get(self, solution_id, query_data):
        """Get comments for the solution"""
        return {}, 501

    @jwt_required()
    @solutions.input(TextBodySchema)
    @solutions.output(CommentOutSchema, status_code=201)
    @solutions.doc(security="jwt_access_token", responses={201: "Comment created"})
    def post(self, solution_id):
        """Create a new comment for the solution. Activated account required."""
        return {}, 501


solutions.add_url_rule(
    "/solutions/<int:solution_id>", view_func=Solution.as_view("solution")
)
solutions.add_url_rule(
    "/solutions/<int:solution_id>/approval",
    view_func=SolutionApproval.as_view("solution_approval"),
)
solutions.add_url_rule(
    "/solutions/<int:solution_id>/reaction",
    view_func=SolutionReaction.as_view("solution_reaction"),
)
solutions.add_url_rule(
    "/solutions/<int:solution_id>/report",
    view_func=SolutionReport.as_view("solution_report"),
)
solutions.add_url_rule(
    "/solutions/<int:solution_id>/comments",
    view_func=SolutionComments.as_view("solution_comments"),
)
