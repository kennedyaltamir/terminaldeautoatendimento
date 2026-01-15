# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 16:00:00
import asyncio
import httpx
import pytest

BASE_URL = "http://localhost:8000/api"

@pytest.mark.asyncio
async def test_1_double_dispatch_lock():
    """Valida Lock Transacional (Double Dispatch)"""
    order_id = "uuid-ready-order"
    h1 = {"Authorization": "Bearer TOKEN_D1"}
    h2 = {"Authorization": "Bearer TOKEN_D2"}
    async with httpx.AsyncClient() as client:
        res = await asyncio.gather(
            client.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=h1),
            client.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=h2),
            return_exceptions=True
        )
        codes = [r.status_code for r in res if not isinstance(r, Exception)]
        assert 200 in codes and 400 in codes

@pytest.mark.asyncio
async def test_2_driver_exclusivity():
    """Valida que um driver não pega dois pedidos simultâneos"""
    headers = {"Authorization": "Bearer TOKEN_D1"}
    async with httpx.AsyncClient() as client:
        await client.patch(f"{BASE_URL}/admin/delivery/orders/ord-1/dispatch", headers=headers)
        res = await client.patch(f"{BASE_URL}/admin/delivery/orders/ord-2/dispatch", headers=headers)
        assert res.status_code == 400

@pytest.mark.asyncio
async def test_3_ownership_security():
    """Valida que apenas o dono do pedido envia GPS"""
    headers = {"Authorization": "Bearer TOKEN_DRIVER_B"}
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/admin/delivery/orders/ord-driver-a/location", 
                                 headers=headers, json={"lat": 0, "lng": 0})
        assert res.status_code == 403

@pytest.mark.asyncio
async def test_8_eta_consistency():
    """Valida decréscimo lógico do ETA"""
    headers = {"Authorization": "Bearer TOKEN_D1"}
    async with httpx.AsyncClient() as client:
        r1 = await client.post(f"{BASE_URL}/admin/delivery/orders/ord-1/location", headers=headers, json={"lat": -19.220, "lng": -44.930})
        r2 = await client.post(f"{BASE_URL}/admin/delivery/orders/ord-1/location", headers=headers, json={"lat": -19.227, "lng": -44.940})
        assert r2.json()["eta_seconds"] < r1.json()["eta_seconds"]
