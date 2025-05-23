"""Add content column to post table.

Revision ID: 6ada2494e1f8
Revises: 17733d8a1645
Create Date: 2025-05-23 00:34:09.391330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ada2494e1f8'
down_revision: Union[str, None] = '17733d8a1645'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass