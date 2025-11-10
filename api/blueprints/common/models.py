import datetime

import sqlalchemy as sa
from sqlalchemy import orm as so


class TimestampMixin:
    """Mixin to add created_at and edited_at timestamps to models."""

    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    edited_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()
    )
