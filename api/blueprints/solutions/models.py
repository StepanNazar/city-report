from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db
from api.blueprints.common.models import TimestampMixin

if TYPE_CHECKING:
    from api.blueprints.auth.models import User
    from api.blueprints.posts.models import Post


class Solution(TimestampMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    body: so.Mapped[str] = so.mapped_column(sa.String(10000), nullable=False)
    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    author: so.Mapped["User"] = so.relationship(back_populates="solutions")
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("post.id"), nullable=False)
    post: so.Mapped["Post"] = so.relationship(back_populates="solutions")

    def __repr__(self):
        return f"<Solution {self.id}: {self.title}>"
