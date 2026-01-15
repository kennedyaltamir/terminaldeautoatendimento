# DOMAIN: DEVOPS_SCRIPTS
import sys
import os
import uuid
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.main import app
from app.database import SessionLocal
from app.models import Company, Category, Product, Table
from app.core.security import create_access_token

client = TestClient(app)

def verify():
    print("🔍 Verificando TASK-GTM-08: Onboarding Zero-Touch & Importador...")

    # 1. Verificar Dependência
    try:
        import bs4
        print("✅ BeautifulSoup4 instalado.")
    except ImportError:
        print("❌ BeautifulSoup4 não encontrado.")
        sys.exit(1)

    # 2. Teste de Criação Automática de Mesa no Registro
    print("🧪 Teste 1: Auto-criação de Mesa no Registro...")
    unique_id = uuid.uuid4().hex[:6]
    slug = f"zero-touch-{unique_id}"
    
    res_reg = client.post("/api/auth/register", json={
        "company_name": f"Zero Touch {unique_id}",
        "company_slug": slug,
        "owner_email": f"zero-{unique_id}@test.com",
        "password": "Password123!",
        "segment": "gastro"
    })
    
    if res_reg.status_code != 201:
        print(f"❌ Falha no registro: {res_reg.text}")
        sys.exit(1)
        
    token = res_reg.json()["access_token"]
    
    # Verificar se a mesa foi criada
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == slug).first()
    table = db.query(Table).filter(Table.company_id == company.id).first()
    
    if table and table.table_number == 1:
        print("✅ Mesa 1 criada automaticamente.")
    else:
        print("❌ Mesa 1 não foi criada.")
        sys.exit(1)
    
    db.close()

    # 3. Teste de Importador (Mockado)
    print("🧪 Teste 2: Importador iFood (Mock)...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Mock do ImporterService para não bater no iFood real
    with patch("app.services.importer_service.ImporterService.import_from_ifood", new_callable=AsyncMock) as mock_import:
        mock_import.return_value = {"status": "success", "imported_items": 10}
        
        res_import = client.post("/api/admin/menu/import/ifood", headers=headers, json={
            "url": "https://www.ifood.com.br/delivery/sao-paulo-sp/restaurante-teste/123"
        })
        
        if res_import.status_code == 200 and res_import.json()["imported_items"] == 10:
            print("✅ Endpoint de importação respondeu corretamente.")
        else:
            print(f"❌ Falha no endpoint de importação: {res_import.text}")
            sys.exit(1)

    print("\n🏆 TASK-GTM-08: VALIDAÇÃO CONCLUÍDA.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
