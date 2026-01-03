from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Category, Company
from datetime import datetime, time

client = TestClient(app)

def test_category_scheduling_logic():
    """
    Testa se categorias agendadas aparecem ou somem conforme o horário.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar Categoria "Almoço" (11:00 - 14:00)
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    cat_lunch = Category(
        company_id=company.id,
        name="Almoço Teste",
        start_time=time(11, 0),
        end_time=time(14, 0),
        availability_days=[0, 1, 2, 3, 4, 5, 6] # Todos os dias
    )
    db.add(cat_lunch)
    db.commit()
    
    # Extrair ID antes de fechar a sessão
    cat_id = cat_lunch.id
    
    db.close()

    # 3. Verificar visibilidade
    res = client.get("/api/hamburgueria-ze/menu")
    assert res.status_code == 200
    data = res.json()
    
    # 4. Testar a atualização via API Admin
    update_payload = {
        "start_time": "18:00:00",
        "end_time": "23:00:00"
    }
    
    patch_res = client.patch(f"/api/admin/menu/categories/{cat_id}", headers=headers, json=update_payload)
    assert patch_res.status_code == 200
    assert patch_res.json()["start_time"] == "18:00:00"