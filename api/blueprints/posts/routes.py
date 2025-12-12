from apiflask import abort
from apiflask.views import MethodView
from flask import url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import joinedload

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
from api.blueprints.locations.routes import get_or_create_locality
from api.blueprints.posts import posts
from api.blueprints.posts.models import Post as PostModel
from api.blueprints.posts.models import PostImage
from api.blueprints.posts.schemas import (
    MapBoundsQuerySchema,
    MapClustersOutSchema,
    PostInSchema,
    PostOutPaginationSchema,
    PostOutSchema,
    PostSortingFilteringSchema,
)
from api.blueprints.users.schemas import ReactionSchema


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
        query = PostModel.query

        locality_id = query_data.get("locality_id")
        locality_provider = query_data.get("locality_provider")
        if locality_id and locality_provider and locality_provider == "nominatim":
            locality = Locality.query.filter_by(osm_id=int(locality_id)).first()
            if locality:
                query = query.filter_by(locality_id=locality.id)
            else:
                # If locality not found, return an empty result by filtering for impossible ID
                query = query.filter_by(locality_id=-1)

        if query_data.get("sort_by") in ["likes", "dislikes"]:
            query_data["sort_by"] = "created_at"  # until reactions are not implemented
        return create_pagination_response(query, PostModel, "posts.posts", **query_data)

    @jwt_required()
    @posts.input(PostInSchema)
    @posts.output(PostOutSchema, status_code=201)
    @posts.doc(security="jwt_access_token", responses={201: "Post created"})
    def post(self, json_data):
        """Create a new post. Activated account required."""
        from api.blueprints.uploads.models import Image

        user_id = int(get_jwt_identity())
        locality = get_or_create_locality(
            json_data["locality_id"], json_data["locality_provider"]
        )

        post_data = {
            k: v
            for k, v in json_data.items()
            if k not in ["locality_id", "locality_provider", "images_ids"]
        }
        new_post = PostModel(
            author_id=user_id,  # type: ignore
            locality_id=locality.id,  # type: ignore
            **post_data,
        )

        db.session.add(new_post)
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

            post_images = [
                PostImage(post_id=new_post.id, image_id=image_id, order=order)  # type: ignore
                for order, image_id in enumerate(json_data["images_ids"])
            ]
            new_post.image_association = post_images

        db.session.commit()

        return new_post, 201, {"Location": url_for("posts.post", post_id=new_post.id)}


class Post(MethodView):
    @posts.output(PostOutSchema)
    def get(self, post_id):
        """Get a post by ID"""
        return PostModel.query.options(
            joinedload(PostModel.locality), joinedload(PostModel.author)
        ).get_or_404(post_id, description="Post not found")

    @jwt_required()
    @posts.input(PostInSchema)
    @posts.output(PostOutSchema)
    @posts.doc(
        security="jwt_access_token", responses={403: "Forbidden", 200: "Post updated"}
    )
    def put(self, post_id, json_data):
        """Update a post by ID. Only the author can update the post."""
        from api.blueprints.uploads.models import Image

        user_id = int(get_jwt_identity())
        post = PostModel.query.options(
            joinedload(PostModel.locality), joinedload(PostModel.author)
        ).get_or_404(post_id, description="Post not found")

        if post.author_id != user_id:
            abort(403, message="You can only update your own posts")

        locality = get_or_create_locality(
            json_data["locality_id"], json_data["locality_provider"]
        )
        post.locality = locality

        for key, value in json_data.items():
            if key not in [
                "locality_id",
                "locality_provider",
                "images_ids",
            ] and hasattr(post, key):
                setattr(post, key, value)

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

        post_images = [
            PostImage(post_id=post_id, image_id=image_id, order=order)  # type: ignore
            for order, image_id in enumerate(json_data.get("images_ids") or [])
        ]
        post.image_association = post_images

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
        user_id = int(get_jwt_identity())
        post = PostModel.query.get_or_404(post_id, description="Post not found")

        if post.author_id != user_id:
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


class MapClusters(MethodView):
    """Get posts clustered for map display based on zoom level and visible bounds."""

    CLUSTER_THRESHOLD_ZOOM = (
        16  # At this zoom level and above, show all posts without clustering
    )

    @posts.input(MapBoundsQuerySchema, location="query")
    @posts.output(MapClustersOutSchema)
    def get(self, query_data):
        """
        Get posts for map display with automatic clustering.

        At high zoom levels (>= 16), returns all individual posts.
        At lower zoom levels, groups nearby posts into clusters.
        """
        min_lat = query_data["min_lat"]
        max_lat = query_data["max_lat"]
        min_lng = query_data["min_lng"]
        max_lng = query_data["max_lng"]
        zoom = query_data["zoom"]

        posts_in_bounds = PostModel.query.filter(
            PostModel.latitude.between(min_lat, max_lat),
            PostModel.longitude.between(min_lng, max_lng),
        ).all()

        total_in_view = len(posts_in_bounds)

        if zoom >= self.CLUSTER_THRESHOLD_ZOOM:
            items = [
                {
                    "type": "post",
                    "id": post.id,
                    "latitude": post.latitude,
                    "longitude": post.longitude,
                    "title": post.title,
                    "authorFirstName": post.author.firstname if post.author else None,
                    "authorLastName": post.author.lastname if post.author else None,
                    "createdAt": post.created_at.isoformat()
                    if post.created_at
                    else None,
                    "thumbnailUrl": post.images[0].url if post.images else None,
                }
                for post in posts_in_bounds
            ]
            return {"items": items, "total_in_view": total_in_view}

        # Calculate grid size based on zoom level
        # Lower zoom = fewer grid divisions, higher zoom = more divisions
        grid_divisions = 25

        lat_step = (max_lat - min_lat) / grid_divisions
        lng_step = (max_lng - min_lng) / grid_divisions

        # Create grid cells and assign posts to them
        grid: dict[tuple[int, int], list] = {}
        for post in posts_in_bounds:
            if lat_step > 0 and lng_step > 0:
                cell_row = min(
                    int((post.latitude - min_lat) / lat_step), grid_divisions - 1
                )
                cell_col = min(
                    int((post.longitude - min_lng) / lng_step), grid_divisions - 1
                )
            else:
                cell_row, cell_col = 0, 0

            key = (cell_row, cell_col)
            if key not in grid:
                grid[key] = []
            grid[key].append(post)

        # Build response items
        items = []
        for (row, col), cell_posts in grid.items():
            cell_min_lat = min_lat + row * lat_step
            cell_max_lat = min_lat + (row + 1) * lat_step
            cell_min_lng = min_lng + col * lng_step
            cell_max_lng = min_lng + (col + 1) * lng_step

            if len(cell_posts) == 1:
                # Single post - return as individual marker
                post = cell_posts[0]
                items.append(
                    {
                        "type": "post",
                        "id": post.id,
                        "latitude": post.latitude,
                        "longitude": post.longitude,
                        "title": post.title,
                        "authorFirstName": post.author.firstname
                        if post.author
                        else None,
                        "authorLastName": post.author.lastname if post.author else None,
                        "createdAt": post.created_at.isoformat()
                        if post.created_at
                        else None,
                        "thumbnailUrl": post.images[0].url if post.images else None,
                    }
                )
            else:
                # Multiple posts - return as cluster
                center_lat = (cell_min_lat + cell_max_lat) / 2
                center_lng = (cell_min_lng + cell_max_lng) / 2
                items.append(
                    {
                        "type": "cluster",
                        "latitude": center_lat,
                        "longitude": center_lng,
                        "count": len(cell_posts),
                        "bounds": {
                            "minLat": cell_min_lat,
                            "maxLat": cell_max_lat,
                            "minLng": cell_min_lng,
                            "maxLng": cell_max_lng,
                        },
                    }
                )

        return {"items": items, "total_in_view": total_in_view}


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
posts.add_url_rule("/posts/map-clusters", view_func=MapClusters.as_view("map_clusters"))
