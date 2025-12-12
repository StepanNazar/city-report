"""fix_post_image_solution_image_autoincrement

Revision ID: 8b290f9fb250
Revises: 8454ddd831b9
Create Date: 2025-12-12 01:06:05.846137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b290f9fb250'
down_revision = '8454ddd831b9'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == 'postgresql':
        # For PostgreSQL: Create sequences and set them as default for id columns
        # This fixes the autoincrement issue that works in SQLite but not in PostgreSQL

        # Fix post_image table
        op.execute(sa.text("CREATE SEQUENCE IF NOT EXISTS post_image_id_seq"))
        op.execute(sa.text("SELECT setval('post_image_id_seq', COALESCE((SELECT MAX(id) FROM post_image), 0) + 1, false)"))
        op.execute(sa.text("ALTER TABLE post_image ALTER COLUMN id SET DEFAULT nextval('post_image_id_seq')"))
        op.execute(sa.text("ALTER SEQUENCE post_image_id_seq OWNED BY post_image.id"))

        # Fix solution_image table
        op.execute(sa.text("CREATE SEQUENCE IF NOT EXISTS solution_image_id_seq"))
        op.execute(sa.text("SELECT setval('solution_image_id_seq', COALESCE((SELECT MAX(id) FROM solution_image), 0) + 1, false)"))
        op.execute(sa.text("ALTER TABLE solution_image ALTER COLUMN id SET DEFAULT nextval('solution_image_id_seq')"))
        op.execute(sa.text("ALTER SEQUENCE solution_image_id_seq OWNED BY solution_image.id"))
    # SQLite handles INTEGER PRIMARY KEY as autoincrement automatically, no action needed


def downgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == 'postgresql':
        op.execute(sa.text("ALTER TABLE post_image ALTER COLUMN id DROP DEFAULT"))
        op.execute(sa.text("DROP SEQUENCE IF EXISTS post_image_id_seq"))

        op.execute(sa.text("ALTER TABLE solution_image ALTER COLUMN id DROP DEFAULT"))
        op.execute(sa.text("DROP SEQUENCE IF EXISTS solution_image_id_seq"))
