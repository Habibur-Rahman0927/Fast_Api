"""add user table

Revision ID: 46b3a90862fa
Revises: f4510082f153
Create Date: 2022-02-12 17:05:38.321151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46b3a90862fa'
down_revision = 'f4510082f153'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id',sa.Integer(), nullable=False),
        sa.Column('email',sa.String(), nullable=False),
        sa.Column('password',sa.String(), nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
