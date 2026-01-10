from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession, Order, OrderStatus
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def setup_pos_env():
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(
        name=f"POS {unique_id}",
        slug=f"pos-{unique_id}",
        owner_email=f"pos-{unique_id}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Mesas
    t1 = Table(company_id=company.id, table_number=1, qr_token="t1")
    t2 = Table(company_id=company.id, table_number=2, qr_token="t2")
    db.add_all([t1, t2])
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    
    return db, company, t1, t2, token

def test_pos_01_table_concurrency():
    """POS-01: Bloqueio de mesa já ocupada"""
    db, company, t1, _, token = setup_pos_env()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Garçom A abre a mesa
    res_a = client.post(f"/api/admin/tables/{t1.id}/open", headers=headers, json={"customer_name": "Cliente A"})
    assert res_a.status_code == 200
    
    # 2. Garçom B tenta abrir a mesma mesa
    res_b = client.post(f"/api/admin/tables/{t1.id}/open", headers=headers, json={"customer_name": "Cliente B"})
    
    # Deve falhar
    assert res_b.status_code == 400
    assert "ocupada" in res_b.json()["detail"]
    db.close()

def test_pos_03_merge_tables():
    """POS-03: Junção de Mesas (Merge)"""
    db, company, t1, t2, token = setup_pos_env()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Ocupar ambas com tokens únicos
    s1_token = str(uuid.uuid4())
    s2_token = str(uuid.uuid4())
    
    s1 = TableSession(company_id=company.id, table_id=t1.id, customer_name="Mesa 1", session_token=s1_token, access_pin="0000", is_active=True)
    s2 = TableSession(company_id=company.id, table_id=t2.id, customer_name="Mesa 2", session_token=s2_token, access_pin="0000", is_active=True)
    db.add_all([s1, s2])
    db.commit()
    
    # Pedidos
    o1 = Order(company_id=company.id, session_id=s1.id, table_id=t1.id, total_amount=100, status=OrderStatus.PENDING)
    o2 = Order(company_id=company.id, session_id=s2.id, table_id=t2.id, total_amount=50, status=OrderStatus.PENDING)
    db.add_all([o1, o2])
    db.commit()
    
    # Merge T1 -> T2
    payload = {"from_table_id": t1.id, "to_table_id": t2.id, "merge": True}
    res = client.post("/api/admin/tables/transfer", headers=headers, json=payload)
    assert res.status_code == 200
    
    # Verificar
    db.refresh(s1)
    db.refresh(s2)
    
    assert s1.is_active is False # Mesa 1 fechou
    assert s2.is_active is True  # Mesa 2 continua
    
    # Pedidos agora devem estar na sessão 2
    orders_s2 = db.query(Order).filter(Order.session_id == s2.id).count()
    assert orders_s2 == 2 # 1 original + 1 transferido
    db.close()

def test_pos_04_quick_sale():
    """POS-04: Venda Balcão (Sem Mesa)"""
    db, company, _, _, token = setup_pos_env()
    
    # Criar produto
    from app.models import Category, Product
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    prod = Product(category_id=cat.id, name="Coxinha", price=5.00)
    db.add(prod)
    db.commit()
    
    payload = {
        "table_id": None, # Sem mesa
        "qr_token": "staff-override",
        "order_type": "takeout",
        "customer_name": "Balcão Rápido",
        "items": [{"product_id": prod.id, "quantity": 2}]
    }
    
    res = client.post(f"/api/{company.slug}/orders", json=payload)
    assert res.status_code == 201
    
    data = res.json()
    assert data["order_type"] == "takeout"
    assert data["table"] is None
    db.close()