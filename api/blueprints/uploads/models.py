from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import orm as so

from api import db
from api.blueprints.posts.models import PostImage
from api.blueprints.solutions.models import SolutionImage


class Image(db.Model):
    id: so.Mapped[UUID] = so.mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    url: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)

    def __repr__(self):
        return f"<Image {self.url}>"


@sa.event.listens_for(PostImage, "after_delete")
@sa.event.listens_for(SolutionImage, "after_delete")
def delete_orphaned_image(mapper, connection, target):
    image_id = target.image_id
    has_post_associations = (
        connection.scalar(
            sa.select(sa.func.count())
            .select_from(PostImage)
            .where(PostImage.image_id == image_id)
        )
        > 0
    )
    has_solution_associations = (
        connection.scalar(
            sa.select(sa.func.count())
            .select_from(SolutionImage)
            .where(SolutionImage.image_id == image_id)
        )
        > 0
    )
    if (not has_post_associations) and (not has_solution_associations):
        from api import get_app

        url = target.image.url
        connection.execute(sa.delete(Image).where(Image.id == image_id))
        get_app().storage_service.delete_file(url)
