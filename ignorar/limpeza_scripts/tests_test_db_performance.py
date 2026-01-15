import pytest
from sqlalchemy import text
from app.database import SessionLocal

def test_critical_indices_exist():
    """
    Verifica se os índices de performance estão ativos no banco de dados.
    Essencial para garantir que o optimize_db.py foi executado com sucesso.
    """
    db = SessionLocal()
    
    # Query para listar índices no PostgreSQL
    query = """
        SELECT indexname 
        FROM pg_indexes 
        WHERE tablename IN ('orders', 'audit_logs', 'order_items');
    """
    
    try:
        results = db.execute(text(query)).fetchall()
        index_names = [r[0] for r in results]
        
        print(f"\n🔍 Índices encontrados: {len(index_names)}")
        
        # Verificações Críticas
        assert "idx_orders_company_status" in index_names, "Índice de KDS faltando!"
        assert "idx_orders_company_created" in index_names, "Índice de Dashboard faltando!"
        assert "idx_audit_logs_company_created" in index_names, "Índice de Auditoria faltando!"
        assert "idx_order_items_order_id" in index_names, "Índice de Itens faltando!"
        
        print("✅ Todos os índices de performance estão operacionais.")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_critical_indices_exist()
