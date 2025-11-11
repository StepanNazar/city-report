from apiflask import Schema
from apiflask.fields import Boolean, DateTime, Integer, String
from apiflask.validators import OneOf

from api.blueprints.common.schemas import CamelCaseSchema, pagination_schema


class CommentOutSchema(CamelCaseSchema):
    id = Integer()
    related_type = String(validate=OneOf(["comment", "solution", "post"]))
    related_id = Integer()
    author_id = Integer()
    author_first_name = String(metadata={"x-faker": "name.firstName"})
    author_last_name = String(metadata={"x-faker": "name.lastName"})
    body = String(metadata={"x-faker": "lorem.paragraphs"})
    created_at = DateTime(metadata={"x-faker": "date.past"})
    edited_at = DateTime(metadata={"x-faker": "date.recent"})
    likes = Integer()
    dislikes = Integer()
    deleted = Boolean()
    replies = Integer()


CommentOutPaginationSchema = pagination_schema(CommentOutSchema)


class CommentSortingSchema(Schema):
    sort_by = String(
        load_default="created_at",
        validate=OneOf(["created_at", "likes", "dislikes", "edited_at"]),
    )
    order = String(
        load_default="desc",
        validate=OneOf(["asc", "desc"]),
    )
