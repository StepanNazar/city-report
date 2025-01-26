import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash

from main import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64))
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64))
    # locality_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey("Locality.id"))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    is_activated: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    activation_code: so.Mapped[str] = so.mapped_column(sa.String(36))

    def __repr__(self):
        return "<User {}>".format(self.email)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
