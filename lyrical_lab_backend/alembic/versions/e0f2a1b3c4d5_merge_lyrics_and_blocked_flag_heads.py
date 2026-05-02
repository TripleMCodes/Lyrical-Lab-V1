"""merge lyrics and blocked flag heads

Revision ID: e0f2a1b3c4d5
Revises: 4f2a8c0d91b3, d48f5ab3e7d9
Create Date: 2026-04-16 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e0f2a1b3c4d5'
down_revision: Union[str, Sequence[str], None] = ('4f2a8c0d91b3', 'd48f5ab3e7d9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
