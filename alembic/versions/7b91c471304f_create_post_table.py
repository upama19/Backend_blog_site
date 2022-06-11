"""create post table

Revision ID: 7b91c471304f
Revises: 
Create Date: 2022-06-08 18:13:32.341812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b91c471304f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
