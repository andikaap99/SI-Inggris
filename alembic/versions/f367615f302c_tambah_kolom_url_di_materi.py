"""tambah kolom url di materi

Revision ID: f367615f302c
Revises: 153c04a7b556
Create Date: 2025-07-22 17:01:09.948715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f367615f302c'
down_revision: Union[str, Sequence[str], None] = '153c04a7b556'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("Materi", "desc", new_column_name="url")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
