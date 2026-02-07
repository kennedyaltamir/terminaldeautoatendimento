"""create companies table

Revision ID: 20260201_create_companies
Revises: <base>
Create Date: 2026-02-01 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '20260201_create_companies'
down_revision = None  # como é a primeira da tabela companies
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'companies',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )

def downgrade():
    op.drop_table('companies')
