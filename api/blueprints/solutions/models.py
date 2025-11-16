from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db
from api.blueprints.common.models import TimestampMixin

if TYPE_CHECKING:
    from api.blueprints.auth.models import User
    from api.blueprints.posts.models import Post
    from api.blueprints.uploads.models import Image


# Association table for many-to-many relationship between solutions and images
solution_image = sa.Table(
    "solution_image",
    db.Model.metadata,
    sa.Column(
        "solution_id",
        sa.Integer,
        sa.ForeignKey("solution.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "image_id",
        sa.Uuid,
        sa.ForeignKey("image.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


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
    images: so.Mapped[list["Image"]] = so.relationship(
        secondary=solution_image, backref="solutions"
    )

    def __repr__(self):
        return f"<Solution {self.id}: {self.title}>"
