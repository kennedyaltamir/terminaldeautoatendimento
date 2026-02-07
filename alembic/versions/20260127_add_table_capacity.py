"""add table capacity
Revision ID: 20260127_add_table_capacity
Revises: 20260124_add_kiosk_fields
Create Date: 2026-01-27 08:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260127_add_table_capacity'
down_revision = '20260124_add_kiosk_fields'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Adiciona coluna de capacidade com default 4
    # Verifica se a coluna já existe para evitar erro em re-execução
    op.execute("ALTER TABLE tables ADD COLUMN IF NOT EXISTS capacity INTEGER NOT NULL DEFAULT 4")

def downgrade() -> None:
    op.drop_column('tables', 'capacity')
