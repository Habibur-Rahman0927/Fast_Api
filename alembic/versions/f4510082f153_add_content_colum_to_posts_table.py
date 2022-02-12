"""add content colum to posts table

Revision ID: f4510082f153
Revises: 00f2eb37f538
Create Date: 2022-02-12 16:57:10.238119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4510082f153'
down_revision = '00f2eb37f538'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
