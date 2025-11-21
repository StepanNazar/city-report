from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy

from api import db
from api.blueprints.common.models import TimestampMixin

if TYPE_CHECKING:
    from api.blueprints.auth.models import User
    from api.blueprints.posts.models import Post
    from api.blueprints.uploads.models import Image


class SolutionImage(db.Model):
    __tablename__ = "solution_image"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    solution_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("solution.id", ondelete="CASCADE")
    )
    image_id: so.Mapped[str] = so.mapped_column(sa.Uuid, sa.ForeignKey("image.id"))
    order: so.Mapped[int] = so.mapped_column(nullable=False)
    solution: so.Mapped["Solution"] = so.relationship(
        back_populates="image_association"
    )
    image: so.Mapped["Image"] = so.relationship(backref="solution_association")


class Solution(TimestampMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    body: so.Mapped[str] = so.mapped_column(sa.String(10000), nullable=False)
    author_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("user.id"), nullable=False
    )
    author: so.Mapped["User"] = so.relationship(back_populates="solutions")
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("post.id"), nullable=False)
    post: so.Mapped["Post"] = so.relationship(back_populates="solutions")
    image_association: so.Mapped[list["SolutionImage"]] = so.relationship(
        back_populates="solution",
        order_by="SolutionImage.order",
        cascade="all, delete-orphan",
    )
    images: AssociationProxy[list["Image"]] = association_proxy(
        "image_association", "image"
    )

    def __repr__(self):
        return f"<Solution {self.id}: {self.title}>"
