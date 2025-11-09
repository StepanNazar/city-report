from collections.abc import Sequence, Set

from apiflask import Schema
from apiflask.fields import URL, Boolean, Field, Integer, Nested, String
from apiflask.validators import Length, OneOf, Range


def snake_to_camel(string):
    parts = string.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


class CamelCaseSchema(Schema):
    """Base schema that auto converts snake_case ⇄ camelCase"""

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = snake_to_camel(field_name)


class LocationHeader(Schema):
    """Schema for headers of 201 responses with Location header"""

    location = URL(metadata={"description": "URL of the created resource"})


def pagination_query_schema(
    default_per_page: int = 20, max_per_page: int = 100
) -> type[Schema]:
    """Create a pagination query schema with specified default per_page and max per_page values."""

    class PaginationQuerySchema(Schema):
        """Schema for pagination query parameters"""

        page = Integer(load_default=1)
        per_page = Integer(
            load_default=default_per_page, validate=Range(min=1, max=max_per_page)
        )

    return PaginationQuerySchema


class PaginationLinksSchema(CamelCaseSchema):
    """Schema for pagination links in the output"""

    self = URL(metadata={"x-faker": "internet.url"})
    first = URL(metadata={"x-faker": "internet.url"})
    next = URL(metadata={"x-faker": "internet.url"})
    prev = URL(metadata={"x-faker": "internet.url"})
    last = URL(metadata={"x-faker": "internet.url"})


class PaginationOutSchema(CamelCaseSchema):
    """Schema for pagination output"""

    links = Nested(PaginationLinksSchema)
    has_prev = Boolean()
    has_next = Boolean()
    page = Integer()
    total_pages = Integer()
    items_per_page = Integer()
    total_items = Integer()


class TextBodySchema(CamelCaseSchema):
    """Schema for text body input"""

    body = String(required=True, validate=Length(min=1, max=10000))


def merge_schemas(*schemas: type[Schema]) -> type[Schema]:
    """Merge multiple query parameters schemas into one schema."""
    MergedSchema = type("MergedSchema", (*schemas,), {})
    return MergedSchema


def pagination_schema(
    schema: type[Schema], exclude: Sequence[str] | Set[str] | None = None
) -> type[Schema]:
    """Create a pagination schema for the given schema."""

    schema_name = schema.__name__
    if schema_name.endswith("Schema"):
        schema_name = schema_name[:-6]
    schema_name = schema_name + "PaginationSchema"
    NewSchema = type(
        schema_name,
        (PaginationOutSchema,),
        {
            "items": Nested(schema(exclude=exclude) if exclude else schema, many=True),
            "__module__": schema.__module__,
        },
    )
    return NewSchema


class JSONPatchSchema(Schema):
    """Schema for JSON Patch operations"""

    op = String(
        required=True,
        validate=OneOf(["add", "remove", "replace", "move", "copy", "test"]),
        metadata={"description": "The operation to perform"},
    )
    path = String(
        required=True,
        metadata={"description": "The path to the target element"},
    )
    value = Field(
        metadata={"description": "The value to be used in the operation"},
    )
    from_path = String(
        data_key="from",
        metadata={"description": "The source path for move/copy operations"},
    )
