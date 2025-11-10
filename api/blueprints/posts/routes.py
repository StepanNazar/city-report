import datetime

from apiflask import abort
from flask import url_for
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


def serialize_post(post: PostModel) -> dict:
    """Serialize a post to dict for response"""
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "latitude": post.latitude,
        "longitude": post.longitude,
        "created_at": post.created_at,
        "updated_at": post.edited_at,
        "author_id": post.author_id,
        "author_link": url_for("users.user", user_id=post.author_id),
        "author_first_name": post.author.firstname,
        "author_last_name": post.author.lastname,
        "locality_nominatim_id": post.locality.osm_id if post.locality else None,
        "locality_google_id": None,
        "likes": 0,
        "dislikes": 0,
        "comments": 0,
    }


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
        page = query_data.get("page", 1)
        per_page = query_data.get("per_page", 50)
        sort_by = query_data.get("sort_by", "likes")
        order = query_data.get("order", "desc")

        query = PostModel.query

        # Apply sorting
        if sort_by == "created_at":
            order_column = PostModel.created_at
        elif sort_by == "edited_at":
            order_column = PostModel.edited_at
        else:
            # For likes, dislikes, we'll just use created_at for now since we don't have those columns yet
            order_column = PostModel.created_at

        if order == "desc":
            query = query.order_by(order_column.desc(), PostModel.id.desc())
        else:
            query = query.order_by(order_column.asc(), PostModel.id.asc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [serialize_post(post) for post in pagination.items],
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "page": pagination.page,
            "items_per_page": per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
            "links": None,
        }

    @jwt_required()
    @posts.input(PostInSchema)
    @posts.output(PostOutSchema, status_code=201)
    @posts.doc(security="jwt_access_token", responses={201: "Post created"})
    def post(self, json_data):
        """Create a new post. Activated account required."""
        current_user = get_current_user()

        # Get or create locality
        locality_id_input = json_data.get("locality_id")
        locality_provider = json_data.get("locality_provider")

        if locality_provider == "nominatim":
            locality = Locality.query.filter_by(osm_id=locality_id_input).first()
            if not locality:
                # For now, we'll just create a placeholder locality
                # In production, you'd fetch from Nominatim service
                locality = Locality(
                    name="Unknown",
                    state="Unknown",
                    country="Unknown",
                    osm_id=locality_id_input,
                )
                db.session.add(locality)
                db.session.flush()
        else:
            abort(501, message="Only nominatim provider is supported")

        # Create post
        new_post = PostModel(
            title=json_data["title"],
            body=json_data["body"],
            latitude=json_data["latitude"],
            longitude=json_data["longitude"],
            author_id=current_user.id,
            locality_id=locality.id,
        )

        db.session.add(new_post)
        db.session.commit()

        response_data = serialize_post(new_post)
        return response_data, 201, {
            "Location": url_for("posts.post", post_id=new_post.id)
        }


class Post(MethodView):
    @posts.output(PostOutSchema)
    def get(self, post_id):
        """Get a post by ID"""
        post = PostModel.query.get(post_id)
        if not post:
            abort(404, message="Post not found")
        return serialize_post(post)

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
        locality_id_input = json_data.get("locality_id")
        locality_provider = json_data.get("locality_provider")

        if locality_provider == "nominatim":
            locality = Locality.query.filter_by(osm_id=locality_id_input).first()
            if not locality:
                locality = Locality(
                    name="Unknown",
                    state="Unknown",
                    country="Unknown",
                    osm_id=locality_id_input,
                )
                db.session.add(locality)
                db.session.flush()
            post.locality_id = locality.id
        else:
            abort(501, message="Only nominatim provider is supported")

        # Update post fields
        post.title = json_data["title"]
        post.body = json_data["body"]
        post.latitude = json_data["latitude"]
        post.longitude = json_data["longitude"]
        post.edited_at = datetime.datetime.now(datetime.UTC)

        db.session.commit()

        return serialize_post(post)

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


def serialize_solution(solution: SolutionModel) -> dict:
    """Serialize a solution to dict for response"""
    return {
        "id": solution.id,
        "title": solution.title,
        "body": solution.body,
        "created_at": solution.created_at,
        "updated_at": solution.edited_at,
        "author_id": solution.author_id,
        "author_link": url_for(
            "users.user", user_id=solution.author_id
        ),
        "author_first_name": solution.author.firstname,
        "author_last_name": solution.author.lastname,
        "likes": 0,
        "dislikes": 0,
        "comments": 0,
        "approved": False,
        "approved_at": None,
    }


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

        page = query_data.get("page", 1)
        per_page = query_data.get("per_page", 5)
        sort_by = query_data.get("sort_by", "likes")
        order = query_data.get("order", "desc")

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
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [serialize_solution(sol) for sol in pagination.items],
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "page": pagination.page,
            "items_per_page": per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
            "links": None,
        }

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
            title=json_data["title"],
            body=json_data["body"],
            author_id=current_user.id,
            post_id=post_id,
        )

        db.session.add(new_solution)
        db.session.commit()

        response_data = serialize_solution(new_solution)
        return response_data, 201, {
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
