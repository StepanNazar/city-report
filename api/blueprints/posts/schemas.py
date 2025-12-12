from apiflask import Schema, validators
from apiflask.fields import (
    UUID,
    DateTime,
    Float,
    Integer,
    List,
    Method,
    Nested,
    Raw,
    String,
)
from apiflask.validators import Length, OneOf, Range
from flask import url_for
from marshmallow import ValidationError, validates_schema

from api.blueprints.common.schemas import (
    URL_METADATA,
    CamelCaseSchema,
    pagination_schema,
)
from api.blueprints.uploads.schemas import ImageLinkOutSchema


class PostBaseSchema(CamelCaseSchema):
    latitude = Float(metadata={"x-faker": "address.latitude"}, required=True)
    longitude = Float(metadata={"x-faker": "address.longitude"}, required=True)
    title = String(
        metadata={"x-faker": "lorem.sentences"},
        required=True,
        validate=Length(min=1, max=100),
    )
    body = String(
        metadata={"x-faker": "lorem.paragraphs"},
        required=True,
        validate=Length(min=1, max=10000),
    )


class PostInSchema(PostBaseSchema):
    locality_id = Integer(
        metadata={"description": "provider's locality id", "example": 3167397},
        required=True,
    )
    locality_provider = String(
        validate=validators.OneOf(["google", "nominatim"]),
        metadata={"enum": ["google", "nominatim"], "example": "nominatim"},
        required=True,
    )
    images_ids = List(UUID(), validate=Length(max=10))


class PostOutSchema(PostBaseSchema):
    id = Integer()
    author_id = Integer()
    author_link = Method("get_author_link", metadata=URL_METADATA)
    author_first_name = String(
        attribute="author.firstname", metadata={"x-faker": "name.firstName"}
    )
    author_last_name = String(
        attribute="author.lastname", metadata={"x-faker": "name.lastName"}
    )
    locality_nominatim_id = Integer(attribute="locality.osm_id")
    locality_google_id = Integer()
    created_at = DateTime(metadata={"x-faker": "date.past"})
    updated_at = DateTime(attribute="edited_at", metadata={"x-faker": "date.recent"})
    likes = Integer(load_default=0, dump_default=0)
    dislikes = Integer(load_default=0, dump_default=0)
    comments = Integer(load_default=0, dump_default=0)
    images = Nested(ImageLinkOutSchema, many=True, attribute="images")

    def get_author_link(self, obj):
        return url_for("users.user", user_id=obj.author_id)


PostOutPaginationSchema = pagination_schema(PostOutSchema, exclude=["body"])


class PostSortingSchema(Schema):
    sort_by = String(
        load_default="likes",
        validate=OneOf(["created_at", "likes", "dislikes", "edited_at"]),
    )
    order = String(
        load_default="desc",
        validate=OneOf(["asc", "desc"]),
    )


class PostSortingFilteringSchema(PostSortingSchema):
    locality_id = String(
        data_key="localityId",
        metadata={"description": "should be used together with localityProvider"},
    )
    locality_provider = String(
        data_key="localityProvider",
        validate=validators.OneOf(["google", "nominatim"]),
        metadata={
            "enum": ["google", "nominatim"],
            "description": "should be used together with localityId",
        },
    )

    @validates_schema
    def validate_locality_fields(self, data, **kwargs):
        """Validate that locality_id and locality_provider are both present or both absent."""
        has_locality_id = "locality_id" in data and data["locality_id"] is not None
        has_locality_provider = (
            "locality_provider" in data and data["locality_provider"] is not None
        )

        if has_locality_id != has_locality_provider:
            raise ValidationError(
                "Both localityId and localityProvider must be specified together or omitted together."
            )


# Map Clusters Schemas
class MapBoundsQuerySchema(CamelCaseSchema):
    """Schema for map bounding box query parameters"""

    min_lat = Float(
        required=True, metadata={"description": "Minimum latitude of visible area"}
    )
    max_lat = Float(
        required=True, metadata={"description": "Maximum latitude of visible area"}
    )
    min_lng = Float(
        required=True, metadata={"description": "Minimum longitude of visible area"}
    )
    max_lng = Float(
        required=True, metadata={"description": "Maximum longitude of visible area"}
    )
    zoom = Integer(
        required=True,
        validate=Range(min=0, max=20),
        metadata={"description": "Current map zoom level"},
    )


class ClusterBoundsSchema(CamelCaseSchema):
    """Schema for cluster bounds - used for zooming into a cluster"""

    min_lat = Float()
    max_lat = Float()
    min_lng = Float()
    max_lng = Float()


class MapPostItemSchema(CamelCaseSchema):
    """Schema for a single post marker on the map"""

    type = String(dump_default="post")
    id = Integer()
    latitude = Float()
    longitude = Float()
    title = String()
    author_first_name = String()
    author_last_name = String()
    created_at = DateTime()
    thumbnail_url = String(allow_none=True)


class MapClusterItemSchema(CamelCaseSchema):
    """Schema for a cluster of posts on the map"""

    type = String(dump_default="cluster")
    latitude = Float(metadata={"description": "Center latitude of the cluster"})
    longitude = Float(metadata={"description": "Center longitude of the cluster"})
    count = Integer(metadata={"description": "Number of posts in the cluster"})
    bounds = Nested(
        ClusterBoundsSchema,
        metadata={"description": "Bounds for zooming into this cluster"},
    )


class MapClustersOutSchema(CamelCaseSchema):
    """Schema for map clusters response"""

    items = List(
        Raw(),
        metadata={
            "description": "List of posts or clusters. Each item has 'type' field: 'post' or 'cluster'"
        },
    )
    total_in_view = Integer(
        metadata={"description": "Total number of posts in the visible area"}
    )
