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
    # Use batch_alter_table to recreate columns with autoincrement=True
    # This works for both SQLite and PostgreSQL

    with op.batch_alter_table('post_image', schema=None) as batch_op:
        batch_op.alter_column('id',
                              existing_type=sa.Integer(),
                              autoincrement=True,
                              existing_nullable=False)

    with op.batch_alter_table('solution_image', schema=None) as batch_op:
        batch_op.alter_column('id',
                              existing_type=sa.Integer(),
                              autoincrement=True,
                              existing_nullable=False)


def downgrade():
    with op.batch_alter_table('post_image', schema=None) as batch_op:
        batch_op.alter_column('id', existing_type=sa.INTEGER(), autoincrement=False, existing_nullable=False)

    with op.batch_alter_table('solution_image', schema=None) as batch_op:
        batch_op.alter_column('id', existing_type=sa.INTEGER(), autoincrement=False, existing_nullable=False)

