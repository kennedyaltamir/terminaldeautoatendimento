import sys
import os
import json
from decimal import Decimal
from fastapi.testclient import TestClient

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.main import app
from app.schemas import ProductCreate, ProductResponse

client = TestClient(app)

def verify():
    print("🔍 Verificando TASK-FIN-01: Refatoração para Centavos...")

    # 1. Teste de Serialização (Output)
    # Cria um modelo Pydantic com valor Decimal e verifica se sai como int
    print("🧪 Teste 1: Serialização de Schema...")
    
    try:
        product = ProductResponse(
            id=1,
            name="Teste Centavos",
            price=Decimal("10.50"), # R$ 10,50
            is_available=True,
            track_stock=False,
            stock_quantity=0
        )
        
        # Dump para JSON (simula resposta da API)
        json_output = product.model_dump(mode='json')
        
        if json_output['price'] == 1050:
            print("✅ Serialização OK: 10.50 -> 1050")
        else:
            print(f"❌ Falha na serialização: Esperado 1050, Recebido {json_output['price']}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erro no teste de serialização: {e}")
        sys.exit(1)

    # 2. Teste de Deserialização (Input)
    print("🧪 Teste 2: Deserialização de Schema...")
    
    try:
        # Simula payload vindo do frontend (em centavos)
        payload = {
            "category_id": 1,
            "name": "Input Test",
            "price": 2590, # R$ 25,90
            "is_available": True
        }
        
        product_create = ProductCreate(**payload)
        
        if product_create.price == Decimal("25.90"):
            print("✅ Deserialização OK: 2590 -> 25.90")
        else:
            print(f"❌ Falha na deserialização: Esperado 25.90, Recebido {product_create.price}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erro no teste de deserialização: {e}")
        sys.exit(1)

    # 3. Verificação de Arquivos Frontend
    print("🧪 Teste 3: Verificação de Arquivos Frontend...")
    
    files_to_check = [
        "frontend/src/lib/utils.ts",
        "frontend/src/context/CartContext.tsx"
    ]
    
    for f in files_to_check:
        if os.path.exists(f):
            print(f"✅ Arquivo encontrado: {f}")
        else:
            print(f"❌ Arquivo faltando: {f}")
            sys.exit(1)

    print("\n🏆 TASK-FIN-01: VALIDAÇÃO CONCLUÍDA.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
