import datetime

import sqlalchemy as sa
from sqlalchemy import orm as so


class TimestampMixin:
    """Mixin to add created_at and edited_at timestamps to models."""

    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    edited_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now()
    )

    @classmethod
    def __declare_last__(cls) -> None:
        @sa.event.listens_for(cls, "before_update", propagate=True)
        def _sqlite_touch_edited_at(mapper, connection, target) -> None:
            if connection.dialect.name == "sqlite":
                target.edited_at = datetime.datetime.now(tz=datetime.UTC)
