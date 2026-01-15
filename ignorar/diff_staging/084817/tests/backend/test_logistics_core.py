# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 17:00:00
import asyncio
import httpx
import pytest

# SSOT: Configurações de Ambiente de Teste
BASE_URL = "http://127.0.0.1:8000/api"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

async def get_auth_token():
    """Obtém um token real do backend para as sessões de teste."""
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{BASE_URL}/auth/token",
            data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}
        )
        if res.status_code != 200:
            raise Exception(f"Falha no setup de autenticação: {res.text}")
        return res.json()["access_token"]

@pytest.fixture(scope="module")
async def auth_headers():
    token = await get_auth_token()
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_1_double_dispatch_lock(auth_headers):
    """Valida Lock Transacional (Double Dispatch)"""
    # 1. Busca um pedido pronto no banco
    async with httpx.AsyncClient(timeout=10.0) as client:
        orders_res = await client.get(f"{BASE_URL}/admin/delivery/orders", headers=auth_headers)
        ready_orders = [o for o in orders_res.json() if o["status"] == "ready"]
        
        if not ready_orders:
            pytest.skip("Nenhum pedido 'ready' disponível para teste de lock.")
            
        order_id = ready_orders[0]["id"]

        # 2. Simula corrida de dois entregadores
        res = await asyncio.gather(
            client.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=auth_headers),
            client.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=auth_headers),
            return_exceptions=True
        )
        
        codes = [r.status_code for r in res if hasattr(r, 'status_code')]
        # Critério L6: Um sucesso (200), um bloqueio de lock (400)
        assert 200 in codes
        assert 400 in codes

@pytest.mark.asyncio
async def test_2_driver_exclusivity(auth_headers):
    """Valida que um driver não pega dois pedidos simultâneos"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        orders_res = await client.get(f"{BASE_URL}/admin/delivery/orders", headers=auth_headers)
        ready_orders = [o for o in orders_res.json() if o["status"] == "ready"]
        
        if len(ready_orders) < 2:
            pytest.skip("Massa de dados insuficiente (precisa de 2 pedidos ready).")

        # Pega o primeiro
        await client.patch(f"{BASE_URL}/admin/delivery/orders/{ready_orders[0]['id']}/dispatch", headers=auth_headers)
        
        # Tenta pegar o segundo (Deve falhar 400)
        res = await client.patch(f"{BASE_URL}/admin/delivery/orders/{ready_orders[1]['id']}/dispatch", headers=auth_headers)
        assert res.status_code == 400
        assert "em andamento" in res.json()["detail"].lower()

@pytest.mark.asyncio
async def test_3_ownership_security(auth_headers):
    """Valida que um usuário comum não pode injetar GPS em pedidos administrativos"""
    # Nota: Este teste exige um token de 'manager' vs 'driver' se o RBAC for estrito.
    # Aqui validamos a rejeição de pedidos inexistentes ou sem atribuição.
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.post(
            f"{BASE_URL}/admin/delivery/orders/00000000-0000-0000-0000-000000000000/location", 
            headers=auth_headers, 
            json={"lat": 0, "lng": 0}
        )
        # Deve retornar 404 (não encontrado) ou 403 (se for de outro driver)
        assert res.status_code in [404, 403]

@pytest.mark.asyncio
async def test_8_eta_consistency(auth_headers):
    """Valida decréscimo lógico do ETA em rota ativa"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        orders_res = await client.get(f"{BASE_URL}/admin/delivery/orders", headers=auth_headers)
        active = [o for o in orders_res.json() if o["status"] == "delivering"]
        
        if not active:
            pytest.skip("Nenhum pedido em rota para validar ETA.")
            
        order_id = active[0]["id"]
        
        # Ponto A (Longe)
        r1 = await client.post(f"{BASE_URL}/admin/delivery/orders/{order_id}/location", headers=auth_headers, json={"lat": -19.220, "lng": -44.930})
        # Ponto B (Perto)
        r2 = await client.post(f"{BASE_URL}/admin/delivery/orders/{order_id}/location", headers=auth_headers, json={"lat": -19.227, "lng": -44.940})
        
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert r2.json()["eta_seconds"] < r1.json()["eta_seconds"]
