"""merge heads

Revision ID: 1d0f7cb8134f
Revises: 20260201_add_cid, 20260201_create_companies, bcbb8a001ade
Create Date: 2026-02-01 22:24:42.343943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d0f7cb8134f'
down_revision: Union[str, None] = ('20260201_add_cid', '20260201_create_companies', 'bcbb8a001ade')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass