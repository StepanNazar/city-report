from apiflask import Schema
from apiflask.fields import URL, DateTime, Float, Integer, List, String
from apiflask.validators import Length, OneOf

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
    author_link = URL()
    author_first_name = String(metadata={"x-faker": "name.firstName"})
    author_last_name = String(metadata={"x-faker": "name.lastName"})
    locality_nominatim_id = Integer()
    locality_google_id = Integer()
    created_at = DateTime(metadata={"x-faker": "date.past"})
    updated_at = DateTime(metadata={"x-faker": "date.recent"})
    likes = Integer()
    dislikes = Integer()
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


class PostSortingFilteringSchema(PostSortingSchema):
    locality_id = String()
