from datetime import datetime, timezone

from apiflask import abort
from apiflask.views import MethodView
from flask import url_for
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import db
from api.blueprints.comments.schemas import (
    CommentOutPaginationSchema,
    CommentOutSchema,
    CommentSortingSchema,
)
from api.blueprints.common.routes import create_pagination_response
from api.blueprints.common.schemas import (
    JSONPatchSchema,
    TextBodySchema,
    merge_schemas,
    pagination_query_schema,
)
from api.blueprints.posts.models import Post as PostModel
from api.blueprints.solutions import solutions
from api.blueprints.solutions.models import Solution as SolutionModel
from api.blueprints.solutions.models import SolutionImage
from api.blueprints.solutions.schemas import (
    SolutionInSchema,
    SolutionOutPaginationSchema,
    SolutionOutSchema,
    SolutionSortingFilteringSchema,
)
from api.blueprints.users.schemas import ReactionSchema


class PostSolutions(MethodView):
    @solutions.input(
        merge_schemas(
            pagination_query_schema(default_per_page=5), SolutionSortingFilteringSchema
        ),
        location="query",
    )
    @solutions.output(SolutionOutPaginationSchema)
    def get(self, post_id, query_data):
        """Get solutions for post"""
        PostModel.query.get_or_404(post_id, description="Post not found")

        query = SolutionModel.query.filter_by(post_id=post_id)

        if query_data.get("approved") is not None:
            query = query.filter_by(approved=query_data["approved"])

        if query_data.get("sort_by") in ["likes", "dislikes"]:
            query_data["sort_by"] = "created_at"  # until reactions are not implemented
        return create_pagination_response(
            query,
            SolutionModel,
            "solutions.post_solutions",
            post_id=post_id,
            **query_data,
        )

    @jwt_required()
    @solutions.input(SolutionInSchema)
    @solutions.output(SolutionOutSchema, status_code=201)
    @solutions.doc(security="jwt_access_token", responses={201: "Solution created"})
    def post(self, post_id, json_data):
        """Create a new solution for post. Activated account required."""
        from api.blueprints.solutions.models import SolutionImage
        from api.blueprints.uploads.models import Image

        user_id = int(get_jwt_identity())
        PostModel.query.get_or_404(post_id, description="Post not found")

        solution_data = {k: v for k, v in json_data.items() if k != "images_ids"}
        new_solution = SolutionModel(
            author_id=user_id,  # type: ignore
            post_id=post_id,  # type: ignore
            **solution_data,
        )

        db.session.add(new_solution)
        db.session.flush()

        if json_data.get("images_ids"):
            existing_image_ids = db.session.scalars(
                db.select(Image.id).where(Image.id.in_(json_data["images_ids"]))
            ).all()
            non_existing_image_ids = set(json_data["images_ids"]) - set(
                existing_image_ids
            )
            if non_existing_image_ids:
                abort(
                    422,
                    message=f"Images with IDs {non_existing_image_ids} do not exist",
                )

            solution_images = [
                SolutionImage(
                    solution_id=new_solution.id,  # type: ignore
                    image_id=image_id,  # type: ignore
                    order=order,  # type: ignore
                )
                for order, image_id in enumerate(json_data["images_ids"])
            ]
            new_solution.image_association = solution_images

        db.session.commit()

        return (
            new_solution,
            201,
            {"Location": url_for("solutions.solution", solution_id=new_solution.id)},
        )


class Solution(MethodView):
    @solutions.output(SolutionOutSchema)
    def get(self, solution_id):
        """Get the solution by ID"""
        return SolutionModel.query.get_or_404(
            solution_id, description="Solution not found"
        )

    @jwt_required()
    @solutions.input(SolutionInSchema)
    @solutions.output(SolutionOutSchema)
    @solutions.doc(
        security="jwt_access_token",
        responses={200: "Solution updated", 403: "Forbidden"},
    )
    def put(self, solution_id, json_data):
        """Update solution. Only the author of the solution can update it"""
        from api.blueprints.uploads.models import Image

        user_id = int(get_jwt_identity())
        solution = SolutionModel.query.get_or_404(
            solution_id, description="Solution not found"
        )

        if solution.author_id != user_id:
            abort(403, message="You can only update your own solutions")

        for key, value in json_data.items():
            if key not in ["images_ids"] and hasattr(solution, key):
                setattr(solution, key, value)

        if json_data.get("images_ids"):
            existing_image_ids = db.session.scalars(
                db.select(Image.id).where(Image.id.in_(json_data["images_ids"]))
            ).all()
            non_existing_image_ids = set(json_data["images_ids"]) - set(
                existing_image_ids
            )
            if non_existing_image_ids:
                abort(
                    422,
                    message=f"Images with IDs {non_existing_image_ids} do not exist",
                )

        solution_images = [
            SolutionImage(solution_id=solution_id, image_id=image_id, order=order)  # type: ignore
            for order, image_id in enumerate(json_data.get("images_ids") or [])
        ]
        solution.image_association = solution_images

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
        user_id = int(get_jwt_identity())
        solution = SolutionModel.query.get_or_404(
            solution_id, description="Solution not found"
        )

        if solution.author_id != user_id:
            abort(403, message="You can only delete your own solutions")

        db.session.delete(solution)
        db.session.commit()

        return "", 204


class SolutionApproval(MethodView):
    @jwt_required()
    @solutions.doc(
        security="jwt_access_token",
        responses={204: "Solution approved", 403: "Forbidden", 404: "Not found"},
    )
    def put(self, solution_id):
        """Approve the solution. Only the author of the post can approve the solution."""
        user_id = int(get_jwt_identity())
        solution = SolutionModel.query.get_or_404(
            solution_id, description="Solution not found"
        )

        if solution.post.author_id != user_id:
            abort(403, message="Only the post author can approve solutions")

        solution.approved = True
        solution.approved_at = datetime.now(timezone.utc)

        db.session.commit()

        return "", 204

    @jwt_required()
    @solutions.doc(
        security="jwt_access_token",
        responses={
            204: "Solution approval removed",
            403: "Forbidden",
            404: "Not found",
        },
    )
    def delete(self, solution_id):
        """Remove approval of the solution. Only the author of the post can remove approval."""
        user_id = int(get_jwt_identity())
        solution = SolutionModel.query.get_or_404(
            solution_id, description="Solution not found"
        )

        if solution.post.author_id != user_id:
            abort(403, message="Only the post author can remove approval")

        solution.approved = False
        solution.approved_at = None

        db.session.commit()

        return "", 204


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
    "/posts/<int:post_id>/solutions", view_func=PostSolutions.as_view("post_solutions")
)
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
