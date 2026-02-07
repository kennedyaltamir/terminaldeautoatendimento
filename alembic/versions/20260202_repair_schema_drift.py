"""repair schema drift

Revision ID: 20260202_repair_drift
Revises: 1d0f7cb8134f
Create Date: 2026-02-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '20260202_repair_drift'
down_revision = '1d0f7cb8134f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c['name'] for c in inspector.get_columns('companies')]

    # 1. Repair: custom_domain
    if 'custom_domain' not in columns:
        op.add_column('companies', sa.Column('custom_domain', sa.String(length=255), nullable=True))
        op.create_index(op.f('ix_companies_custom_domain'), 'companies', ['custom_domain'], unique=True)

    # 2. Repair: kiosk_password_hash (Frequentemente esquecido)
    if 'kiosk_password_hash' not in columns:
        op.add_column('companies', sa.Column('kiosk_password_hash', sa.String(length=255), nullable=True))

    # 3. Repair: logo_url & banner_url
    if 'logo_url' not in columns:
        op.add_column('companies', sa.Column('logo_url', sa.String(length=500), nullable=True))
    if 'banner_url' not in columns:
        op.add_column('companies', sa.Column('banner_url', sa.String(length=500), nullable=True))

    # 4. Repair: whatsapp fields
    if 'whatsapp_api_url' not in columns:
        op.add_column('companies', sa.Column('whatsapp_api_url', sa.String(length=500), nullable=True))
    if 'whatsapp_instance' not in columns:
        op.add_column('companies', sa.Column('whatsapp_instance', sa.String(length=100), nullable=True))
    if 'whatsapp_token' not in columns:
        op.add_column('companies', sa.Column('whatsapp_token', sa.String(length=500), nullable=True))

    # 5. Repair: payment & fees
    if 'payment_provider' not in columns:
        op.add_column('companies', sa.Column('payment_provider', sa.String(length=50), server_default='none', nullable=False))
    if 'payment_credentials' not in columns:
        op.add_column('companies', sa.Column('payment_credentials', sa.JSON(), nullable=True))
    if 'pix_key' not in columns:
        op.add_column('companies', sa.Column('pix_key', sa.String(length=255), nullable=True))
    if 'mp_access_token' not in columns:
        op.add_column('companies', sa.Column('mp_access_token', sa.String(length=255), nullable=True))
    if 'mp_user_id' not in columns:
        op.add_column('companies', sa.Column('mp_user_id', sa.String(length=50), nullable=True))
    
    # 6. Repair: Fiscal
    if 'cnpj' not in columns:
        op.add_column('companies', sa.Column('cnpj', sa.String(length=20), nullable=True))
    if 'inscricao_estadual' not in columns:
        op.add_column('companies', sa.Column('inscricao_estadual', sa.String(length=20), nullable=True))
    if 'fiscal_token' not in columns:
        op.add_column('companies', sa.Column('fiscal_token', sa.String(length=255), nullable=True))
    if 'csc_token' not in columns:
        op.add_column('companies', sa.Column('csc_token', sa.String(length=100), nullable=True))
    if 'csc_id' not in columns:
        op.add_column('companies', sa.Column('csc_id', sa.String(length=10), nullable=True))

    # 7. Repair: Timestamps & Operational
    if 'opens_at' not in columns:
        op.add_column('companies', sa.Column('opens_at', sa.Time(), nullable=True))
    if 'closes_at' not in columns:
        op.add_column('companies', sa.Column('closes_at', sa.Time(), nullable=True))

def downgrade() -> None:
    # Em caso de downgrade, removemos apenas se existirem
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c['name'] for c in inspector.get_columns('companies')]

    if 'custom_domain' in columns:
        op.drop_index(op.f('ix_companies_custom_domain'), table_name='companies')
        op.drop_column('companies', 'custom_domain')
    
    if 'kiosk_password_hash' in columns:
        op.drop_column('companies', 'kiosk_password_hash')

