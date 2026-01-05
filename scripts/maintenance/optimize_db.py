import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import engine

def apply_optimization():
    """Aplica índices de performance em tabelas de alto volume."""
    print("🚀 Otimizando Banco de Dados MesaFlow...")

    commands = [
        # 1. Índices para Dashboard e KDS (Tabela Orders)
        "CREATE INDEX IF NOT EXISTS idx_orders_company_status ON orders (company_id, status);",
        "CREATE INDEX IF NOT EXISTS idx_orders_company_created ON orders (company_id, created_at);",
        
        # 2. Índices para Auditoria (Tabela AuditLogs)
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_company_created ON audit_logs (company_id, created_at);",
        
        # 3. Índices para Itens de Pedido (Agilizar carregamento de detalhes)
        "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items (order_id);",
        
        # 4. Índice para Carteira Digital (Lookups por telefone)
        "CREATE INDEX IF NOT EXISTS idx_wallet_lookup ON customer_wallets (company_id, customer_phone);"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"  [OK] {cmd.split(' ON ')[1] if ' ON ' in cmd else cmd}")
            except Exception as e:
                print(f"  [AVISO] Erro no comando: {str(e)[:50]}...")
        conn.commit()

    print("\n✨ Banco de dados otimizado com sucesso!")

if __name__ == "__main__":
    apply_optimization()
