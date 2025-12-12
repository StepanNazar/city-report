from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db

if TYPE_CHECKING:
    from api.blueprints.auth.models import User
    from api.blueprints.posts.models import Post


class Locality(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    latitude: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    longitude: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    osm_id: so.Mapped[int] = so.mapped_column(sa.Integer, unique=True, nullable=True)
    users: so.Mapped[list["User"]] = so.relationship(back_populates="locality")
    posts: so.Mapped[list["Post"]] = so.relationship(back_populates="locality")

    def __repr__(self):
        return f"<Locality id={self.id} lat={self.latitude} lon={self.longitude}>"
