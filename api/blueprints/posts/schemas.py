from apiflask import Schema
from apiflask.fields import URL, Boolean, DateTime, Float, Integer, List, String
from apiflask.validators import OneOf
from marshmallow.validate import Length

from api.blueprints.common.schemas import CamelCaseSchema, pagination_schema


class PostInSchema(CamelCaseSchema):
    latitude = Float(metadata={"x-faker": "address.latitude"}, required=True)
    longitude = Float(metadata={"x-faker": "address.longitude"}, required=True)
    locality_id = String(metadata={"x-faker": "address.city"}, required=True)
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


class PostOutSchema(PostInSchema):
    id = Integer()
    author_id = Integer()
    author_name = String(metadata={"x-faker": "name.firstName"})
    author_last_name = String(metadata={"x-faker": "name.lastName"})
    country_id = String(metadata={"x-faker": "address.country"}, required=True)
    state_id = String(metadata={"x-faker": "address.state"}, required=True)
    country = String(metadata={"x-faker": "address.country"})
    state = String(metadata={"x-faker": "address.state"})
    locality = String(metadata={"x-faker": "address.city"})
    created_at = DateTime(metadata={"x-faker": "date.past"})
    edited_at = DateTime(metadata={"x-faker": "date.recent"})
    likes = Integer()
    dislikes = Integer()
    deleted = Boolean()
    comments = Integer()


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
    locality_id = String(required=True)


class PostSortingFilteringSchema(PostSortingSchema):
    locality_id = String(required=True)
