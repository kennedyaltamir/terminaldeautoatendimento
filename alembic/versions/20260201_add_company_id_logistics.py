# DOMAIN: DATABASE / MIGRATIONS
# VERSION: 1.0.0
# DESCRIPTION: Adiciona coluna company_id na tabela logistics_journeys para suporte a RLS.
"""add company_id to logistics_journeys
Revision ID: 20260201_add_cid
Revises: 3107224d31a2
Create Date: 2026-02-01 00:30:00.000000
"""
from alembic import op
import sqlalchemy as sa
import app.models.core

revision = '20260201_add_cid'
down_revision = '3107224d31a2'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Adiciona a coluna permitindo nulos inicialmente para não quebrar dados existentes
    op.add_column('logistics_journeys', sa.Column('company_id', app.models.core.GUID(), nullable=True))
    
    # Vincula o company_id dos pedidos às jornadas existentes (Data Migration)
    op.execute("""
        UPDATE logistics_journeys 
        SET company_id = orders.company_id 
        FROM orders 
        WHERE logistics_journeys.order_id = orders.id
    """)
    
    # Torna obrigatório após a migração de dados
    op.alter_column('logistics_journeys', 'company_id', nullable=False)
    
    # Adiciona chave estrangeira e índice
    op.create_foreign_key('fk_logistics_company', 'logistics_journeys', 'companies', ['company_id'], ['id'])
    op.create_index('idx_logistics_journeys_company', 'logistics_journeys', ['company_id'])

def downgrade() -> None:
    op.drop_index('idx_logistics_journeys_company', table_name='logistics_journeys')
    op.drop_constraint('fk_logistics_company', 'logistics_journeys', type_='foreignkey')
    op.drop_column('logistics_journeys', 'company_id')

