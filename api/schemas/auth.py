from apiflask import Schema, validators
from apiflask.fields import Boolean, DateTime, Email, Integer, String

from api import models


class AccessTokenSchema(Schema):
    access_token = String()


class PasswordSchema(Schema):
    password = String(
        required=True,
        validate=validators.Length(min=8, max=models.PASSWORD_MAX_LENGTH),
        # pattern="^regex$", validate in both api and database?
        metadata={"example": "Pas$word123"},
    )


class LoginSchema(PasswordSchema):
    email = Email(
        required=True,
        metadata={"example": "dsx@gmail.com"},
    )


class RegisterSchema(LoginSchema):
    name = String(
        required=True, metadata={"example": "John", "description": "first name"}
    )
    lastName = String(
        required=True, metadata={"example": "Doe", "description": "last name"}
    )


class UserSchema(Schema):
    id = Integer()
    name = String(attribute="firstname", metadata={"x-faker": "name.firstName"})
    lastName = String(attribute="lastname", metadata={"x-faker": "name.lastName"})
    email = Email(
        validate=validators.Email(), metadata={"x-faker": "internet.email"}
    )  # is validation needed for output?
    isActivated = Boolean(attribute="is_activated")


class DeviceSchema(Schema):
    id = Integer()
    ip = String(attribute="ip_address", metadata={"x-faker": "internet.ip"})
    device = String()
    os = String()
    browser = String()
    loginTime = DateTime(attribute="login_time", metadata={"x-faker": "date.recent"})
