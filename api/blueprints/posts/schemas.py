from apiflask import Schema, validators
from apiflask.fields import URL, DateTime, Float, Integer, List, Method, String
from apiflask.validators import Length, OneOf
from flask import url_for
from marshmallow import ValidationError, validates_schema

from api.blueprints.common.schemas import CamelCaseSchema, pagination_schema
from api.blueprints.locations.schemas import locality_provider


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
    images_links = List(URL(metadata={"x-faker": "image.city"}))


class PostInSchema(PostBaseSchema):
    locality_id = Integer(metadata={"description": "provider's locality id", "example": 3167397}, required=True)
    locality_provider = locality_provider


class PostOutSchema(PostBaseSchema):
    id = Integer()
    author_id = Integer()
    author_link = Method("get_author_link")
    author_first_name = String(attribute="author.firstname", metadata={"x-faker": "name.firstName"})
    author_last_name = String(attribute="author.lastname", metadata={"x-faker": "name.lastName"})
    locality_nominatim_id = Integer(attribute="locality.osm_id")
    locality_google_id = Method("get_locality_google_id")
    created_at = DateTime(metadata={"x-faker": "date.past"})
    updated_at = DateTime(attribute="edited_at", metadata={"x-faker": "date.recent"})
    likes = Integer(load_default=0, dump_default=0)
    dislikes = Integer(load_default=0, dump_default=0)
    comments = Integer(load_default=0, dump_default=0)

    def get_author_link(self, obj):
        return url_for("users.user", user_id=obj.author_id)

    def get_locality_google_id(self, obj):
        return None  # Not implemented yet


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
    locality_id = String(data_key="localityId")
    locality_provider = String(
        data_key="localityProvider",
        validate=validators.OneOf(["google", "nominatim"]),
        metadata={"enum": ["google", "nominatim"], "example": "nominatim"},
    )

    @validates_schema
    def validate_locality_fields(self, data, **kwargs):
        """Validate that locality_id and locality_provider are both present or both absent."""
        has_locality_id = "locality_id" in data and data["locality_id"] is not None
        has_locality_provider = "locality_provider" in data and data["locality_provider"] is not None

        if has_locality_id != has_locality_provider:
            raise ValidationError(
                "Both localityId and localityProvider must be specified together or omitted together."
            )
