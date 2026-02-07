"""create companies table (base schema)

Revision ID: 20260202_create_companies
Revises: None
Create Date: 2026-02-02 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = '20260202_create_companies'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'companies',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('plan_tier', sa.String(50)),
        sa.Column('segment', sa.String(50)),
        sa.Column('qr_config', sa.JSON),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('companies')
