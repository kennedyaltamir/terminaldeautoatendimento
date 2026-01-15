from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_system_health():
    """
    Teste de fumaça (Smoke Test) para garantir que os componentes principais
    estão respondendo após todas as alterações.
    """

    # 1. API Root
    res_root = client.get("/")
    assert res_root.status_code == 200
    # Atualizado para a versão atual
    assert "v2.3.1" in res_root.json()["message"]

    # 2. Cardápio Público (Leitura)
    res_menu = client.get("/api/hamburgueria-ze/menu")
    assert res_menu.status_code == 200
    data = res_menu.json()
    assert "categories" in data
    assert len(data["categories"]) > 0

    # 3. Autenticação (Admin)
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. KDS (Admin Protegido)
    res_kds = client.get("/api/admin/hamburgueria-ze/orders", headers=headers)
    assert res_kds.status_code == 200
    assert isinstance(res_kds.json(), list)

    # 5. Métricas (Admin Protegido)
    res_metrics = client.get("/api/admin/metrics", headers=headers)
    assert res_metrics.status_code == 200
    assert "total_revenue" in res_metrics.json()

    print("\n✅ Sistema Operacional e Estável!")
