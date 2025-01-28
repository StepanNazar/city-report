import sqlalchemy as sa
import sqlalchemy.orm as so
from ua_parser import parse
from werkzeug.security import generate_password_hash, check_password_hash

from api import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64))
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64))
    # locality_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey("Locality.id"))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    is_activated: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    # add expiration for activation code?
    activation_code: so.Mapped[str] = so.mapped_column(sa.String(36))  # use sa.UUID instead?
    active_devices: so.Mapped[list["ActiveDevice"]] = so.relationship()

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class ActiveDevice(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    refresh_jti: so.Mapped[str] = so.mapped_column(sa.String(36),
                                                   index=True, unique=True)  # use sa.UUID instead?
    access_jti: so.Mapped[str] = so.mapped_column(sa.String(36),
                                                  index=True, unique=True)  # use sa.UUID instead?
    login_time: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, default=sa.func.now())
    expires_at: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime)  # to do: implement deletion of expired records
    ip_address: so.Mapped[str] = so.mapped_column(sa.String(15))  # is there a better type?
    device: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    os: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    browser: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))

    def __init__(self, *args, user_agent: str = None, ip_address: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        user_agent = parse(user_agent)
        self.device = user_agent.device.family if user_agent.device else None
        self.os = user_agent.os.family if user_agent.os else None
        self.browser = user_agent.user_agent.family if user_agent.user_agent else None
        self.ip_address = ip_address

    def __repr__(self):
        return f"<ActiveDevice {self.ip_address} {self.os} {self.browser}>"
