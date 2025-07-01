from apiflask import Schema
from apiflask.fields import DateTime, Integer, List, String
from apiflask.validators import OneOf

from api.schemas.common import CamelCaseSchema, pagination_schema


class AICommentSchema(CamelCaseSchema):
    id = Integer()
    post_id = Integer()
    body = String(metadata={"x-faker": "lorem.paragraphs"})
    created_at = DateTime(metadata={"x-faker": "date.past"})


class APIKeySchema(CamelCaseSchema):
    api_key = String(required=True)


class AIPromptSchema(CamelCaseSchema):
    text = String(metadata={"x-faker": "lorem.paragraphs"}, required=True)


class LocalityIDListSchema(CamelCaseSchema):
    ids = List(Integer())


class AIDataSuggestionSchema(CamelCaseSchema):
    locality_id = Integer()
    author_id = Integer()
    author_first_name = String(metadata={"x-faker": "name.firstName"})
    author_last_name = String(metadata={"x-faker": "name.lastName"})
    body = String(metadata={"x-faker": "lorem.paragraphs"})
    created_at = DateTime(metadata={"x-faker": "date.past"})


class AIDataSuggestionSortingSchema(Schema):
    order = String(
        load_default="desc",
        validate=OneOf(["asc", "desc"]),
    )


# filtering by author can be added
AIDataSuggestionPaginationSchema = pagination_schema(AIDataSuggestionSchema)
