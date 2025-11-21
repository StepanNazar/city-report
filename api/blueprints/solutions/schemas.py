from apiflask import Schema
from apiflask.fields import (
    UUID,
    Boolean,
    DateTime,
    Integer,
    List,
    Method,
    Nested,
    String,
)
from apiflask.validators import Length, OneOf
from flask import url_for

from api.blueprints.common.schemas import (
    URL_METADATA,
    CamelCaseSchema,
    pagination_schema,
)
from api.blueprints.uploads.schemas import ImageLinkOutSchema


class SolutionBaseSchema(CamelCaseSchema):
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


class SolutionInSchema(SolutionBaseSchema):
    images_ids = List(UUID(), validate=Length(max=10))


class SolutionOutSchema(SolutionBaseSchema):
    id = Integer()
    author_id = Integer()
    author_link = Method("get_author_link", metadata=URL_METADATA)
    author_first_name = String(
        attribute="author.firstname", metadata={"x-faker": "name.firstName"}
    )
    author_last_name = String(
        attribute="author.lastname", metadata={"x-faker": "name.lastName"}
    )
    created_at = DateTime(metadata={"x-faker": "date.past"})
    updated_at = DateTime(attribute="edited_at", metadata={"x-faker": "date.recent"})
    likes = Integer(load_default=0, dump_default=0)
    dislikes = Integer(load_default=0, dump_default=0)
    comments = Integer(load_default=0, dump_default=0)
    approved = Boolean(load_default=False, dump_default=False)
    approved_at = DateTime(metadata={"x-faker": "date.recent"})
    images = Nested(ImageLinkOutSchema, many=True, attribute="images")

    def get_author_link(self, obj):
        return url_for("users.user", user_id=obj.author_id)


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
