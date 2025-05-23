"""Add user table.

Revision ID: 955f764ed9d8
Revises: 6ada2494e1f8
Create Date: 2025-05-23 00:41:06.134102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '955f764ed9d8'
down_revision: Union[str, None] = '6ada2494e1f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
