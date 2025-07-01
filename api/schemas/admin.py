from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import OneOf

from api.schemas.auth import PasswordSchema
from api.schemas.common import CamelCaseSchema, pagination_schema


class CreateAdminSchema(PasswordSchema):
    admin_id = Integer(required=True)


class ReportSchema(CamelCaseSchema):
    id = Integer()
    body = String(metadata={"x-faker": "lorem.paragraph"})
    related_type = String(validate=OneOf(["comment", "solution", "post"]))
    related_id = Integer()
    reported_by_id = Integer()
    reported_by_first_name = String(metadata={"x-faker": "name.firstName"})
    reported_by_last_name = String(metadata={"x-faker": "name.lastName"})
    reported_user_id = Integer()
    reported_user_first_name = String(metadata={"x-faker": "name.firstName"})
    reported_user_last_name = String(metadata={"x-faker": "name.lastName"})
    report_time = String(metadata={"x-faker": "date.past"})


ReportPaginationSchema = pagination_schema(ReportSchema)


class ReportSortingFilteringSchema(Schema):
    order = String(
        load_default="desc",
        validate=OneOf(["asc", "desc"]),
    )
    related_type = String(validate=OneOf(["post", "solution", "comment"]))
