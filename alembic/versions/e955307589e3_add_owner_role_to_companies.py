"""add_owner_role_to_companies

Revision ID: 20260202_add_owner_role
Revises: 20260202_fix_phone
Create Date: 2026-02-02 14:30:00.000000
"""

from alembic import op
import sqlalchemy as sa

# Revisão identificadora
revision = '20260202_add_owner_role'
down_revision = '20260202_fix_phone'
branch_labels = None
depends_on = None

def upgrade():
    # Adiciona a coluna owner_role à tabela companies
    op.add_column('companies', sa.Column('owner_role', sa.String(length=50), nullable=True))

def downgrade():
    # Remove a coluna se precisar reverter
    op.drop_column('companies', 'owner_role')
