"""add column to post

Revision ID: 239d7e4c325d
Revises: 7b91c471304f
Create Date: 2022-06-08 18:27:57.728333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '239d7e4c325d'
down_revision = '7b91c471304f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('Content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
