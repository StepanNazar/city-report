from apiflask import Schema
from apiflask.fields import URL, Boolean, DateTime, Integer, List, String
from apiflask.validators import Length, OneOf

from api.blueprints.common.schemas import CamelCaseSchema, pagination_schema


class SolutionInSchema(CamelCaseSchema):
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


class SolutionOutSchema(SolutionInSchema):
    id = Integer()
    author_id = Integer()
    author_link = URL()
    author_first_name = String(metadata={"x-faker": "name.firstName"})
    author_last_name = String(metadata={"x-faker": "name.lastName"})
    created_at = DateTime(metadata={"x-faker": "date.past"})
    updated_at = DateTime(metadata={"x-faker": "date.recent"})
    likes = Integer()
    dislikes = Integer()
    comments = Integer()
    approved = Boolean()
    approved_at = DateTime(metadata={"x-faker": "date.recent"})


SolutionOutPaginationSchema = pagination_schema(SolutionOutSchema)


class SolutionSortingFilteringSchema(Schema):
    sort_by = String(
        load_default="likes",
        validate=OneOf(["created_at", "likes", "dislikes", "edited_at"]),
    )
    order = String(
        load_default="desc",
        validate=OneOf(["asc", "desc"]),
    )
    approved = Boolean()
