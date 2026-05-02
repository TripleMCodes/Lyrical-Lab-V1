"""add API request limit table

Revision ID: f1a2b3c4d5e6
Revises: 9f8e7d6c5b4a
Create Date: 2026-04-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, Sequence[str], None] = '9f8e7d6c5b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add API request limits table."""
    op.create_table('api_request_limits',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('request_count', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('date_created', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    sa.ForeignKeyConstraint(['user_id'], ['users.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_api_request_limits_user_id', 'api_request_limits', ['user_id'])
    op.create_index('ix_api_request_limits_date_created', 'api_request_limits', ['date_created'])


def downgrade() -> None:
    """Downgrade schema - remove API request limits table."""
    op.drop_index('ix_api_request_limits_date_created', table_name='api_request_limits')
    op.drop_index('ix_api_request_limits_user_id', table_name='api_request_limits')
    op.drop_table('api_request_limits')
