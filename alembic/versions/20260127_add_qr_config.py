# DOMAIN: ROOT_CONFIG
# LAST_MODIFIED: 2026-01-27 16:15:00
"""add qr_config to companies

Revision ID: 20260127_add_qr_config
Revises: 20260127_add_table_capacity
Create Date: 2026-01-27 16:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260127_add_qr_config'
down_revision = '20260127_add_table_capacity'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Adiciona a coluna qr_config na tabela companies
    # Usamos JSONB se disponível (Postgres), senão JSON genérico
    op.add_column('companies', sa.Column('qr_config', sa.JSON(), nullable=True))

def downgrade() -> None:
    op.drop_column('companies', 'qr_config')