from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus
from decimal import Decimal
import uuid
import time

client = TestClient(app)

def test_backend_handles_rapid_sync():
    """
    Simula o comportamento do 'Sync Engine' do frontend:
    O frontend envia vários pedidos em sequência rápida assim que a rede volta.
    O backend deve aceitar todos sem conflito de chave ou erro de concorrência.
    """
    
    # 1. Setup
    unique_slug = f"sync-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Sync Corp",
        slug=unique_slug,
        owner_email=f"sync-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    company_id = company.id
    db.close()

    # 2. Simular Fila de Pedidos Offline (Payloads)
    offline_queue = []
    for i in range(5):
        offline_queue.append({
            "table_id": None, # Sem mesa
            "order_type": "takeout", # <--- CORREÇÃO: Especificar tipo para não exigir mesa
            "qr_token": "staff-override",
            "customer_name": f"Offline Customer {i}",
            "payment_method": "cash",
            "items": [] 
        })

    # 3. Disparo Rápido (Simulando o loop do useOfflineSync)
    responses = []
    start_time = time.time()
    
    for payload in offline_queue:
        res = client.post(f"/api/{unique_slug}/orders", json=payload)
        responses.append(res)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n⚡ Sincronizados 5 pedidos em {duration:.4f} segundos.")

    # 4. Validação
    success_count = 0
    for res in responses:
        if res.status_code == 201:
            success_count += 1
        else:
            print(f"❌ Falha: {res.text}")

    assert success_count == 5, "Nem todos os pedidos foram sincronizados corretamente."

    # Verificar no Banco
    db = SessionLocal()
    count = db.query(Order).filter(Order.company_id == company_id).count()
    assert count == 5
    db.close()