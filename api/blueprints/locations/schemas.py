from apiflask.fields import DateTime, Integer, String
from apiflask.validators import Length

from api.blueprints.common.schemas import CamelCaseSchema, pagination_schema


class CountrySchema(CamelCaseSchema):
    id = Integer()
    name = String(
        metadata={"x-faker": "address.country"}, validate=Length(min=1, max=100)
    )
    users = Integer()
    posts = Integer()
    approved_solutions = Integer()
    states = Integer()
    created_at = DateTime(metadata={"x-faker": "date.past"})


class StateSchema(CamelCaseSchema):
    id = Integer()
    name = String(
        metadata={"x-faker": "address.state"}, validate=Length(min=1, max=100)
    )
    country_id = Integer()
    users = Integer()
    posts = Integer()
    approved_solutions = Integer()
    localities = Integer()
    created_at = DateTime(metadata={"x-faker": "date.past"})


class LocalitySchema(CamelCaseSchema):
    id = Integer()
    name = String(metadata={"x-faker": "address.city"}, validate=Length(min=1, max=100))
    country_id = Integer()
    state_id = Integer()
    users = Integer()
    posts = Integer()
    approved_solutions = Integer()
    created_at = DateTime(metadata={"x-faker": "date.past"})


class LocationNameInputSchema(CamelCaseSchema):
    name = String(validate=Length(min=1, max=100), required=True)


CountryPaginationSchema = pagination_schema(CountrySchema)
StatePaginationSchema = pagination_schema(StateSchema)
LocalityPaginationSchema = pagination_schema(LocalitySchema)
