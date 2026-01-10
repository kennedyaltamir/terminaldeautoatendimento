from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_dashboard_routes_integrity():
    """
    Valida se todas as rotas descritas na Especificação Funcional (DASHBOARD_BEHAVIOR.md)
    estão respondendo corretamente na API (Backend).
    Isso garante que o Frontend não terá 'Links Quebrados' ou dados faltantes.
    """
    
    # 1. Setup
    unique_slug = f"spec-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Spec Corp",
        slug=unique_slug,
        owner_email=f"spec-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 2. Mapeamento de Rotas da Especificação -> Endpoints da API
    # (Nota: Algumas rotas de frontend consomem múltiplos endpoints, aqui testamos os principais)
    routes_to_test = [
        # Dashboard
        ("/api/admin/metrics", 200),
        
        # Franquia
        ("/api/admin/franchise/dashboard", 200),
        
        # Menu (Categorias e Produtos)
        (f"/api/{unique_slug}/menu", 200), # Público
        
        # Estoque
        ("/api/admin/inventory/ingredients", 200),
        ("/api/admin/inventory/shopping-list", 200),
        
        # Mesas
        ("/api/admin/tables/dashboard", 200),
        
        # Equipe
        ("/api/admin/employees", 200),
        
        # Histórico
        (f"/api/admin/{unique_slug}/history", 200),
        
        # Configurações
        ("/api/admin/company/me", 200)
    ]

    print(f"\n🔍 Validando integridade das rotas da Especificação...")
    
    for route, expected_status in routes_to_test:
        res = client.get(route, headers=headers)
        
        if res.status_code == expected_status:
            print(f"✅ [OK] {route}")
        else:
            print(f"❌ [FALHA] {route} - Esperado {expected_status}, Recebido {res.status_code}")
            print(f"   Detalhe: {res.text}")
            assert False, f"Rota quebrada: {route}"

    print("✨ Todas as rotas críticas da especificação estão ativas!")
