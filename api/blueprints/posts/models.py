from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy

from api import db
from api.blueprints.common.models import TimestampMixin

if TYPE_CHECKING:
    from api.blueprints.auth.models import User
    from api.blueprints.locations.models import Locality
    from api.blueprints.solutions.models import Solution
    from api.blueprints.uploads.models import Image


class PostImage(db.Model):
    __tablename__ = "post_image"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    post_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("post.id", ondelete="CASCADE")
    )
    image_id: so.Mapped[str] = so.mapped_column(sa.Uuid, sa.ForeignKey("image.id"))
    order: so.Mapped[int] = so.mapped_column(sa.SmallInteger, nullable=False)
    post: so.Mapped["Post"] = so.relationship(back_populates="image_association")
    image: so.Mapped["Image"] = so.relationship(backref="post_association")


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
    image_association: so.Mapped[list["PostImage"]] = so.relationship(
        back_populates="post", order_by="PostImage.order", cascade="all, delete-orphan"
    )
    images: AssociationProxy[list["Image"]] = association_proxy(
        "image_association", "image"
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"
