"""Create post table

Revision ID: 17733d8a1645
Revises: 
Create Date: 2025-05-23 00:19:02.857187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17733d8a1645'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass