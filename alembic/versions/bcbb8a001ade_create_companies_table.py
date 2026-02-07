"""create companies table
Revision ID: bcbb8a001ade
Revises: 20260108_9999
Create Date: 2026-02-01 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'bcbb8a001ade'
down_revision = '20260108_9999'
branch_labels = None
depends_on = None

def upgrade():
    # 🛡️ DEFENSIVE UPGRADE: Check if table exists before creating
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    
    if 'companies' not in tables:
        op.create_table(
            'companies',
            sa.Column('id', psql.UUID(as_uuid=True), primary_key=True),
            sa.Column('name', sa.String(255), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        )
    else:
        # Table exists, ensure columns match expectation or just log
        print("⚠️ Table 'companies' already exists. Skipping creation.")

def downgrade():
    op.drop_table('companies')
