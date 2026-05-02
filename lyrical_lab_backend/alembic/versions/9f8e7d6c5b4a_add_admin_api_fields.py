"""add admin api fields

Revision ID: 9f8e7d6c5b4a
Revises: e0f2a1b3c4d5
Create Date: 2026-04-16 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9f8e7d6c5b4a'
down_revision: Union[str, Sequence[str], None] = 'e0f2a1b3c4d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('admin', sa.Column('api_key', sa.String(length=255), nullable=True))
    op.add_column('admin', sa.Column('api_url', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('admin', 'api_url')
    op.drop_column('admin', 'api_key')
