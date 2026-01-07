import sys
import os
from sqlalchemy import text
from pathlib import Path

# Ajuste de Path para encontrar o app.database
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from app.database import engine

def fix_all_enums():
    """
    Normaliza TODOS os dados de colunas baseadas em Enum para lowercase no PostgreSQL.
    Cobre tabelas operacionais, de auditoria e de configuração.
    """
    print("🚀 [SRE] Iniciando Normalização Atômica de Enums...")

    # Mapeamento exaustivo: (Tabela, Coluna, Nome do Tipo no Postgres)
    normalization_tasks = [
        # Configurações e Empresa
        ("companies", "plan_tier", "plantier"),
        ("companies", "segment", "companysegment"),
        ("companies", "payment_provider", "paymentprovider"),
        
        # Operacional e Pedidos
        ("orders", "status", "orderstatus"),
        ("orders", "order_type", "ordertype"),
        ("orders", "payment_method", "paymentmethod"),
        ("orders", "payment_status", "paymentstatus"),
        ("orders", "origin", "orderorigin"),
        
        # Serviços e Chamados (Onde ocorreu o erro 'BILL')
        ("service_requests", "service_type", "servicetype"),
        
        # Auditoria (Onde ocorreu o erro 'DELETE')
        ("audit_logs", "action", "auditaction"),
        
        # Equipe e Logística
        ("employees", "role", "userrole"),
        ("driver_ledger", "type", "ledgertype"),
        
        # Menu e Estoque
        ("products", "station", "productstation"),
        ("ingredients", "unit", "unitofmeasure"),
        
        # Marketing
        ("promotions", "discount_type", "discounttype"),
    ]

    with engine.connect() as conn:
        for table, column, type_name in normalization_tasks:
            print(f"🔍 Processando {table}.{column}...")
            try:
                # Lógica de normalização: Cast para texto -> Lowercase -> Cast de volta para o Enum
                # Nota: PaymentProvider é o único que mantemos em UPPERCASE conforme o Model.py
                target_case = "UPPER" if column == "payment_provider" else "LOWER"
                
                sql = f"""
                UPDATE {table} 
                SET {column} = {target_case}({column}::text)::{type_name} 
                WHERE {column} IS NOT NULL;
                """
                
                result = conn.execute(text(sql))
                conn.commit()
                
                if result.rowcount > 0:
                    print(f"   ✅ {result.rowcount} linhas corrigidas.")
                else:
                    print(f"   ℹ️  Dados já normalizados.")
                    
            except Exception as e:
                conn.rollback()
                # Erro comum: a tabela ou coluna pode não existir ainda dependendo da versão do banco
                if "does not exist" in str(e):
                    print(f"   ⏭️  Pulado: Coluna ou Tabela não encontrada.")
                else:
                    print(f"   ⚠️  Erro: {str(e).splitlines()[0]}")
        
    print("\n🎉 [SRE] Limpeza de dados concluída! O sistema deve estar estável agora.")

if __name__ == "__main__":
    fix_all_enums()
