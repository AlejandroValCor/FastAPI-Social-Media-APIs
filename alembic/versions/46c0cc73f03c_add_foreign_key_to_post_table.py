"""Add foreign-key to post table.

Revision ID: 46c0cc73f03c
Revises: 955f764ed9d8
Create Date: 2025-05-23 00:58:04.827804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46c0cc73f03c'
down_revision: Union[str, None] = '955f764ed9d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE'
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass