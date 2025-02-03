import datetime
import re
from uuid import uuid4

import sqlalchemy as sa
import sqlalchemy.orm as so
from email_validator import validate_email
from flask import current_app
from ua_parser import parse
from werkzeug.security import generate_password_hash, check_password_hash

from api import db

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128  # prevent DoS attacks with long passwords


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64))
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64))  # validation for names?
    # locality_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey("Locality.id"))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    is_activated: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    # add expiration for activation code? restrict unactivated accounts?
    activation_code: so.Mapped[str] = so.mapped_column(sa.String(36),  # use sa.UUID instead?
                                                       default=lambda: str(uuid4()))
    active_devices: so.Mapped[list["ActiveDevice"]] = so.relationship()

    @so.validates("email")
    def email_validator(self, key, email: str) -> str:
        return validate_email(email).normalized

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        return cls.query.filter_by(email=validate_email(email).normalized).one_or_none()

    def __init__(self, password: str = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_password(password)

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password: str) -> None:
        # prohibit non-ASCII characters?
        # to do: replace assert with raise because assert is debug-only
        if len(password) < PASSWORD_MIN_LENGTH:
            raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters long")
        if len(password) > PASSWORD_MAX_LENGTH:
            raise ValueError(f"Password must be at most {PASSWORD_MAX_LENGTH} characters long")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\W", password):
            raise ValueError("Password must contain at least one special character")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not isinstance(password, str):
            return False
        if len(password) > PASSWORD_MAX_LENGTH:
            return False
        return check_password_hash(self.password_hash, password)


class ActiveDevice(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    refresh_jti: so.Mapped[str] = so.mapped_column(sa.String(36),
                                                   index=True, unique=True)  # use sa.UUID instead?
    access_jti: so.Mapped[str] = so.mapped_column(sa.String(36),
                                                  index=True, unique=True)  # use sa.UUID instead?
    login_time: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, default=sa.func.now())
    expires_at: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime,
        default=lambda: datetime.datetime.now(datetime.UTC) +
                        current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    )  # to do: implement deletion of expired records
    ip_address: so.Mapped[str] = so.mapped_column(sa.String(15))  # is there a better type?
    device: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    os: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    browser: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))

    def __init__(self, *args, user_agent: str = '', ip_address: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        user_agent = parse(user_agent)
        self.device = user_agent.device.family if user_agent.device else None
        self.os = user_agent.os.family if user_agent.os else None
        self.browser = user_agent.user_agent.family if user_agent.user_agent else None
        self.ip_address = ip_address

    def __repr__(self):
        return f"<ActiveDevice {self.ip_address} {self.os} {self.browser}>"
