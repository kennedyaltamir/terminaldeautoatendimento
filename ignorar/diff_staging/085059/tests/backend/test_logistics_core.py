# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 17:40:00
import asyncio
import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000/api"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

@pytest.fixture(scope="module")
async def auth_headers():
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{BASE_URL}/auth/token",
            data={"username": ADMIN_EMAIL, "password": ADMIN_PASS}
        )
        token = res.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_1_double_dispatch_lock(auth_headers):
    """Valida Lock Transacional (Double Dispatch)"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Busca ou cria pedido ready
        orders_res = await client.get(f"{BASE_URL}/admin/delivery/orders", headers=auth_headers)
        ready = [o for o in orders_res.json() if o["status"] == "ready"]
        
        if not ready:
            # Seed de emergência para teste
            pytest.skip("Execute o seed para ter pedidos 'ready'.")
            
        order_id = ready[0]["id"]
        res = await asyncio.gather(
            client.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=auth_headers),
            client.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=auth_headers),
            return_exceptions=True
        )
        codes = [r.status_code for r in res if hasattr(r, 'status_code')]
        assert 200 in codes
        assert 400 in codes

@pytest.mark.asyncio
async def test_8_eta_consistency(auth_headers):
    """Valida decréscimo lógico do ETA"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        orders_res = await client.get(f"{BASE_URL}/admin/delivery/orders", headers=auth_headers)
        delivering = [o for o in orders_res.json() if o["status"] == "delivering"]
        
        if not delivering:
            pytest.skip("Nenhum pedido em rota.")
            
        order_id = delivering[0]["id"]
        r1 = await client.post(f"{BASE_URL}/admin/delivery/orders/{order_id}/location", headers=auth_headers, json={"lat": -19.220, "lng": -44.930})
        r2 = await client.post(f"{BASE_URL}/admin/delivery/orders/{order_id}/location", headers=auth_headers, json={"lat": -19.227, "lng": -44.940})
        
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert r2.json()["eta_seconds"] < r1.json()["eta_seconds"]
