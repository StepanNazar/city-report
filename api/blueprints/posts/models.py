import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db

if TYPE_CHECKING:
    from api.blueprints.auth.models import User
    from api.blueprints.locations.models import Locality
    from api.blueprints.solutions.models import Solution


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    body: so.Mapped[str] = so.mapped_column(sa.String(10000), nullable=False)
    latitude: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    longitude: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    edited_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()
    )
    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    author: so.Mapped["User"] = so.relationship(back_populates="posts")
    locality_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("locality.id"), nullable=False)
    locality: so.Mapped["Locality"] = so.relationship(back_populates="posts")
    solutions: so.Mapped[list["Solution"]] = so.relationship(
        back_populates="post", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"
