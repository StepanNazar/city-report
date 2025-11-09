from apiflask import Schema, validators
from apiflask.fields import Boolean, DateTime, Email, Integer, String

from api.schemas.common import CamelCaseSchema

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128


class AccessTokenSchema(Schema):
    access_token = String()


class PasswordSchema(CamelCaseSchema):
    password = String(
        required=True,
        validate=[
            validators.Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH),
            # prohibit non-ASCII characters?
            validators.Regexp(
                r".*\d.*", error="Password must contain at least one digit"
            ),
            validators.Regexp(
                r".*[A-Z].*",
                error="Password must contain at least one uppercase letter",
            ),
            validators.Regexp(
                r".*[a-z].*",
                error="Password must contain at least one lowercase letter",
            ),
            validators.Regexp(
                r".*\W.*", error="Password must contain at least one special character"
            ),
        ],
        metadata={"example": "Pas$word123"},
    )


class LoginSchema(PasswordSchema):
    email = Email(
        required=True,
        metadata={"example": "dsx@gmail.com"},
        validate=validators.Email(),
    )


class RegisterSchema(LoginSchema):
    first_name = String(
        required=True, metadata={"example": "John", "description": "first name"}
    )
    last_name = String(
        required=True, metadata={"example": "Doe", "description": "last name"}
    )
    locality_id = Integer(
        metadata={"description": "provider's locality id", "example": 3167397}
    )
    locality_provider = String(
        validate=validators.OneOf(["google", "nominatim"]),
        metadata={"enum": ["google", "nominatim"], "example": "nominatim"},
    )


class WhoAmISchema(CamelCaseSchema):
    id = Integer()
    first_name = String(attribute="firstname", metadata={"x-faker": "name.firstName"})
    last_name = String(attribute="lastname", metadata={"x-faker": "name.lastName"})
    email = Email(metadata={"x-faker": "internet.email"})
    is_activated = Boolean()
    locality_nominatim_id = Integer(attribute="locality.osm_id")
    locality_google_id = Integer()
    created_at = DateTime(metadata={"x-faker": "date.past"})


class DeviceSchema(CamelCaseSchema):
    id = Integer()
    ip = String(attribute="ip_address", metadata={"x-faker": "internet.ip"})
    device = String()
    os = String()
    browser = String()
    login_time = DateTime(metadata={"x-faker": "date.recent"})
