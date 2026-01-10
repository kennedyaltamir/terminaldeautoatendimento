from app.models import Order
from sqlalchemy import inspect

def test_order_indices_exist():
    """Verifica se os índices compostos foram definidos no modelo Order."""
    
    # Inspeciona a tabela mapeada pelo SQLAlchemy
    mapper = inspect(Order)
    
    # Obtém os argumentos da tabela (__table_args__)
    # Nota: Em algumas versões do SQLAlchemy, isso pode estar em mapper.local_table.indexes
    indexes = mapper.local_table.indexes
    
    index_names = [i.name for i in indexes]
    
    print(f"Índices encontrados: {index_names}")
    
    assert "idx_orders_company_status" in index_names, "Índice de KDS faltando"
    assert "idx_orders_company_created" in index_names, "Índice de Dashboard faltando"
