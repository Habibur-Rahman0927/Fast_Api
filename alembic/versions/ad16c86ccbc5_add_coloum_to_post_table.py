"""add coloum  to post table

Revision ID: ad16c86ccbc5
Revises: 1bcb3d04bc09
Create Date: 2022-02-12 17:22:46.204509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad16c86ccbc5'
down_revision = '1bcb3d04bc09'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
