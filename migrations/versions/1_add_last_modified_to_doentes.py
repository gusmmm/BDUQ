"""add last_modified to doentes

Revision ID: 000000000001
Revises: c09ffe49f37c
Create Date: 2025-09-03 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '000000000001'
down_revision: Union[str, Sequence[str], None] = 'c09ffe49f37c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add last_modified column.

    Note: SQLite cannot add a column with a non-constant default.
    Strategy:
    - Add the column as nullable with no server default.
    - Backfill existing rows with CURRENT_TIMESTAMP.
    - Leave it nullable (the model sets it on insert/update in Python).
    """
    op.add_column(
        'doentes',
        sa.Column(
            'last_modified',
            sa.DateTime(),
            nullable=True,
        ),
    )
    # Backfill existing rows
    op.execute(sa.text("UPDATE doentes SET last_modified = CURRENT_TIMESTAMP WHERE last_modified IS NULL"))


def downgrade() -> None:
    """Downgrade schema: drop last_modified column."""
    op.drop_column('doentes', 'last_modified')
