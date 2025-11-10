import datetime

import requests
from apiflask import abort
from flask import request, url_for
from flask.views import MethodView
from flask_jwt_extended import get_current_user, jwt_required

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
from api.blueprints.locations.models import Locality
from api.blueprints.posts import posts
from api.blueprints.posts.models import Post as PostModel
from api.blueprints.posts.schemas import (
    PostInSchema,
    PostOutPaginationSchema,
    PostOutSchema,
    PostSortingFilteringSchema,
)
from api.blueprints.solutions.models import Solution as SolutionModel
from api.blueprints.solutions.schemas import (
    SolutionInSchema,
    SolutionOutPaginationSchema,
    SolutionOutSchema,
    SolutionSortingFilteringSchema,
)
from api.blueprints.users.schemas import ReactionSchema


def get_or_create_locality(locality_id, locality_provider):
    """Get or create a locality based on provider and ID."""
    # Import here to avoid circular imports
    from api.services import NominatimService

    if locality_provider == "nominatim":
        locality = Locality.query.filter_by(osm_id=locality_id).first()
        if not locality:
            try:
                name, state, country = (
                    NominatimService.get_locality_name_state_and_country(locality_id)
                )
            except ValueError:
                abort(400, message="Invalid locality id")
            except requests.RequestException:
                abort(500, message="Nominatim service unavailable")
            locality = Locality(
                name=name,
                state=state,
                country=country,
                osm_id=locality_id,
            )
            db.session.add(locality)
            db.session.flush()
        return locality
    else:
        abort(501, message="Only nominatim provider is supported")


class Posts(MethodView):
    @posts.input(
        merge_schemas(
            pagination_query_schema(default_per_page=50), PostSortingFilteringSchema
        ),
        location="query",
    )
    @posts.output(PostOutPaginationSchema)
    def get(self, query_data):
        """Get all posts"""
        sort_by = query_data.get("sort_by")
        order = query_data.get("order")
        locality_id = query_data.get("locality_id")

        query = PostModel.query

        # Apply locality filtering if provided
        if locality_id:
            locality = Locality.query.filter_by(osm_id=int(locality_id)).first()
            if locality:
                query = query.filter_by(locality_id=locality.id)
            # If locality not found, query will return no results naturally

        # Apply sorting
        if sort_by == "created_at":
            order_column = PostModel.created_at
        elif sort_by == "edited_at":
            order_column = PostModel.edited_at
        else:
            # For likes, dislikes, we'll just use created_at for now
            order_column = PostModel.created_at

        if order == "desc":
            query = query.order_by(order_column.desc(), PostModel.id.desc())
        else:
            query = query.order_by(order_column.asc(), PostModel.id.asc())

        # Paginate
        pagination = query.paginate()

        return create_pagination_response(
            pagination, "posts.posts", **request.args
        )

    @jwt_required()
    @posts.input(PostInSchema)
    @posts.output(PostOutSchema, status_code=201)
    @posts.doc(security="jwt_access_token", responses={201: "Post created"})
    def post(self, json_data):
        """Create a new post. Activated account required."""
        current_user = get_current_user()

        # Get or create locality
        locality = get_or_create_locality(
            json_data["locality_id"], json_data["locality_provider"]
        )

        # Create post
        new_post = PostModel(
            author_id=current_user.id,
            locality_id=locality.id,
            **{k: v for k, v in json_data.items() if k not in ["locality_id", "locality_provider"]}
        )

        db.session.add(new_post)
        db.session.commit()

        return new_post, 201, {
            "Location": url_for("posts.post", post_id=new_post.id)
        }


class Post(MethodView):
    @posts.output(PostOutSchema)
    def get(self, post_id):
        """Get a post by ID"""
        post = PostModel.query.get(post_id)
        if not post:
            abort(404, message="Post not found")
        return post

    @jwt_required()
    @posts.input(PostInSchema)
    @posts.output(PostOutSchema)
    @posts.doc(
        security="jwt_access_token", responses={403: "Forbidden", 200: "Post updated"}
    )
    def put(self, post_id, json_data):
        """Update a post by ID. Only the author can update the post."""
        current_user = get_current_user()
        post = PostModel.query.get(post_id)

        if not post:
            abort(404, message="Post not found")

        if post.author_id != current_user.id:
            abort(403, message="You can only update your own posts")

        # Update locality if changed
        locality = get_or_create_locality(
            json_data["locality_id"], json_data["locality_provider"]
        )
        post.locality_id = locality.id

        # Update post fields dynamically
        for key, value in json_data.items():
            if key not in ["locality_id", "locality_provider"] and hasattr(post, key):
                setattr(post, key, value)

        post.edited_at = datetime.datetime.now(datetime.UTC)

        db.session.commit()

        return post

    @jwt_required()
    @posts.input(JSONPatchSchema)
    @posts.output(PostOutSchema)
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
        current_user = get_current_user()
        post = PostModel.query.get(post_id)

        if not post:
            abort(404, message="Post not found")

        if post.author_id != current_user.id:
            abort(403, message="You can only delete your own posts")

        db.session.delete(post)
        db.session.commit()

        return "", 204


class PostReaction(MethodView):
    @jwt_required()
    @posts.input(ReactionSchema)
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
    @posts.input(TextBodySchema)
    @posts.doc(security="jwt_access_token", responses={201: "Report created"})
    def post(self, post_id):
        """Report post. Activated account required."""
        return {}, 501


class PostComments(MethodView):
    @posts.input(
        merge_schemas(pagination_query_schema(), CommentSortingSchema), location="query"
    )
    @posts.output(CommentOutPaginationSchema)
    def get(self, post_id, query_data):
        """Get comments for post"""
        return {}, 501

    @jwt_required()
    @posts.input(TextBodySchema)
    @posts.output(CommentOutSchema, status_code=201)
    @posts.doc(security="jwt_access_token", responses={201: "Comment created"})
    def post(self, post_id):
        """Create a new comment for the post. Activated account required."""
        return {}, 501


class PostSolutions(MethodView):
    @posts.input(
        merge_schemas(
            pagination_query_schema(default_per_page=5), SolutionSortingFilteringSchema
        ),
        location="query",
    )
    @posts.output(SolutionOutPaginationSchema)
    def get(self, post_id, query_data):
        """Get solutions for post"""
        post = PostModel.query.get(post_id)
        if not post:
            abort(404, message="Post not found")

        sort_by = query_data.get("sort_by")
        order = query_data.get("order")

        query = SolutionModel.query.filter_by(post_id=post_id)

        # Apply sorting
        if sort_by == "created_at":
            order_column = SolutionModel.created_at
        elif sort_by == "edited_at":
            order_column = SolutionModel.edited_at
        else:
            # For likes, dislikes, we'll just use created_at for now
            order_column = SolutionModel.created_at

        if order == "desc":
            query = query.order_by(order_column.desc(), SolutionModel.id.desc())
        else:
            query = query.order_by(order_column.asc(), SolutionModel.id.asc())

        # Paginate
        pagination = query.paginate()

        return create_pagination_response(
            pagination, "posts.post_solutions", post_id=post_id, **request.args
        )

    @jwt_required()
    @posts.input(SolutionInSchema)
    @posts.output(SolutionOutSchema, status_code=201)
    @posts.doc(security="jwt_access_token", responses={201: "Solution created"})
    def post(self, post_id, json_data):
        """Create a new solution for post. Activated account required."""
        current_user = get_current_user()

        # Check if post exists
        post = PostModel.query.get(post_id)
        if not post:
            abort(404, message="Post not found")

        # Create solution
        new_solution = SolutionModel(
            author_id=current_user.id,
            post_id=post_id,
            **json_data
        )

        db.session.add(new_solution)
        db.session.commit()

        return new_solution, 201, {
            "Location": url_for(
                "solutions.solution", solution_id=new_solution.id
            )
        }


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
