"""add kiosk fields

Revision ID: 20260124_add_kiosk_fields
Revises: df6d85a95a4f
Create Date: 2026-01-24 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260124_add_kiosk_fields'
down_revision = 'df6d85a95a4f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Adiciona pickup_note em orders
    op.add_column('orders', sa.Column('pickup_note', sa.String(length=255), nullable=True))
    
    # Adiciona payload em payment_transactions
    op.add_column('payment_transactions', sa.Column('payload', sa.JSON(), nullable=True))

def downgrade() -> None:
    op.drop_column('payment_transactions', 'payload')
    op.drop_column('orders', 'pickup_note')

