from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db
from api.blueprints.common.models import TimestampMixin

if TYPE_CHECKING:
    from api.blueprints.auth.models import User
    from api.blueprints.locations.models import Locality
    from api.blueprints.solutions.models import Solution
    from api.blueprints.uploads.models import Image


post_image = sa.Table(
    "post_image",
    db.Model.metadata,
    sa.Column(
        "post_id",
        sa.Integer,
        sa.ForeignKey("post.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "image_id",
        sa.Uuid,
        sa.ForeignKey("image.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Post(TimestampMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    body: so.Mapped[str] = so.mapped_column(sa.String(10000), nullable=False)
    latitude: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    longitude: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    author_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("user.id"), nullable=False
    )
    author: so.Mapped["User"] = so.relationship(back_populates="posts")
    locality_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("locality.id"), nullable=False
    )
    locality: so.Mapped["Locality"] = so.relationship(back_populates="posts")
    solutions: so.Mapped[list["Solution"]] = so.relationship(
        back_populates="post", cascade="all, delete-orphan"
    )
    images: so.Mapped[list["Image"]] = so.relationship(
        secondary=post_image, backref="posts"
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"
