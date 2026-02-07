"""emergency add owner_phone

Revision ID: 20260202_fix_phone
Revises: 20260202_repair_drift
Create Date: 2026-02-02 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '20260202_fix_phone'
down_revision = '20260202_repair_drift'
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c['name'] for c in inspector.get_columns('companies')]

    # 🛡️ REPAIR: Adiciona owner_phone se não existir
    if 'owner_phone' not in columns:
        op.add_column('companies', sa.Column('owner_phone', sa.String(length=20), nullable=True))
        print("✅ Coluna 'owner_phone' restaurada com sucesso.")

def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c['name'] for c in inspector.get_columns('companies')]

    if 'owner_phone' in columns:
        op.drop_column('companies', 'owner_phone')

