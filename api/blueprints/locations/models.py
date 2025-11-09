from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db

if TYPE_CHECKING:
    from api.blueprints.auth.models import User


class Locality(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    state: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    country: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    osm_id: so.Mapped[int] = so.mapped_column(sa.Integer, unique=True, nullable=True)
    users: so.Mapped[list["User"]] = so.relationship(back_populates="locality")

    def __repr__(self):
        return f"<Locality {self.name}, {self.state}, {self.country}>"
