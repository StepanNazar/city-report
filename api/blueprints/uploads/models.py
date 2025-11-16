from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db


class Image(db.Model):
    id: so.Mapped[UUID] = so.mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    url: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)

    def __repr__(self):
        return f"<Image {self.url}>"
