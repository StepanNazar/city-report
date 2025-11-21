"""fix many to many image tables primary keys

Revision ID: 7c21b2821ac4
Revises: 9629633a14fa
Create Date: 2025-11-21 23:39:42.063885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c21b2821ac4'
down_revision = '9629633a14fa'
branch_labels = None
depends_on = None


def upgrade():
    # Fix post_image table
    with op.batch_alter_table('post_image', schema=None) as batch_op:
        batch_op.drop_constraint('pk_post_image', type_='primary')
        batch_op.create_primary_key('pk_post_image', ['id'])

    # Fix solution_image table
    with op.batch_alter_table('solution_image', schema=None) as batch_op:
        batch_op.drop_constraint('pk_solution_image', type_='primary')
        batch_op.create_primary_key('pk_solution_image', ['id'])



def downgrade():
    # Revert solution_image table
    with op.batch_alter_table('solution_image', schema=None) as batch_op:
        batch_op.drop_constraint('pk_solution_image', type_='primary')
        batch_op.create_primary_key('pk_solution_image', ['solution_id', 'image_id'])

    # Revert post_image table
    with op.batch_alter_table('post_image', schema=None) as batch_op:
        batch_op.drop_constraint('pk_post_image', type_='primary')
        batch_op.create_primary_key('pk_post_image', ['post_id', 'image_id'])
