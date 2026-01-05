import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import engine

def apply_optimization():
    """Aplica índices de performance críticos para escalabilidade."""
    print("🚀 Otimizando Banco de Dados (Indices)...")

    commands = [
        # Índices para busca rápida de pedidos
        "CREATE INDEX IF NOT EXISTS idx_orders_company_status ON orders (company_id, status);",
        "CREATE INDEX IF NOT EXISTS idx_orders_company_created ON orders (company_id, created_at DESC);",
        
        # Índices para auditoria
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_company_created ON audit_logs (company_id, created_at DESC);",
        
        # Índices para menu e estoque
        "CREATE INDEX IF NOT EXISTS idx_product_category_id ON products (category_id);",
        "CREATE INDEX IF NOT EXISTS idx_ingredients_company_id ON ingredients (company_id);",
        "CREATE INDEX IF NOT EXISTS idx_options_group_id ON options (group_id);",
        
        # Índices de performance para recursos de UVP
        "CREATE INDEX IF NOT EXISTS idx_customer_wallet_lookup ON customer_wallets (company_id, customer_phone);",
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                print(f"  [OK] Índice criado/verificado: {cmd.split(' ON ')}")
            except Exception as e:
                # Ignora erros de índice já existente (comum em execuções repetidas)
                if "already exists" in str(e):
                    print(f"  [INFO] Índice já existe.")
                else:
                    print(f"  [AVISO] Erro inesperado: {str(e)[:80]}...")
        conn.commit()

    print("\n✨ Banco de dados otimizado com sucesso!")

if __name__ == "__main__":
    apply_optimization()
