# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 16:50:00
import asyncio
import httpx
import pytest

# FIX: Força 127.0.0.1 para evitar problemas de resolução de localhost no Windows
BASE_URL = "http://127.0.0.1:8000/api"

@pytest.mark.asyncio
async def test_1_double_dispatch_lock():
    """Valida Lock Transacional (Double Dispatch)"""
    # Nota: Em teste real, você deve criar um pedido antes ou usar um ID fixo do seed
    order_id = "b143c399-acba-44e4-8ad4-41b2160ae023" # ID de exemplo do seu log
    h1 = {"Authorization": "Bearer TOKEN_VALIDO"}
    h2 = {"Authorization": "Bearer TOKEN_VALIDO"}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            res = await asyncio.gather(
                client.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=h1),
                client.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=h2),
                return_exceptions=True
            )
            codes = [r.status_code for r in res if hasattr(r, 'status_code')]
            # Um deve passar (200), outro deve falhar por lock (400)
            assert 200 in codes
            assert 400 in codes
        except Exception as e:
            pytest.fail(f"Erro de conexão com o backend: {e}")

@pytest.mark.asyncio
async def test_2_driver_exclusivity():
    """Valida que um driver não pega dois pedidos simultâneos"""
    headers = {"Authorization": "Bearer TOKEN_VALIDO"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Pedido 1
        await client.patch(f"{BASE_URL}/admin/delivery/orders/ord-1/dispatch", headers=headers)
        # Pedido 2 (Deve falhar 400)
        res = await client.patch(f"{BASE_URL}/admin/delivery/orders/ord-2/dispatch", headers=headers)
        assert res.status_code == 400

@pytest.mark.asyncio
async def test_3_ownership_security():
    """Valida que apenas o dono do pedido envia GPS"""
    # Tenta enviar localização com token de um driver que não é o dono do pedido
    headers = {"Authorization": "Bearer TOKEN_DRIVER_B"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.post(f"{BASE_URL}/admin/delivery/orders/ord-do-driver-a/location", 
                                 headers=headers, json={"lat": 0, "lng": 0})
        assert res.status_code == 403

@pytest.mark.asyncio
async def test_8_eta_consistency():
    """Valida decréscimo lógico do ETA"""
    headers = {"Authorization": "Bearer TOKEN_VALIDO"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Ponto A (Longe)
        r1 = await client.post(f"{BASE_URL}/admin/delivery/orders/ord-1/location", headers=headers, json={"lat": -19.220, "lng": -44.930})
        # Ponto B (Perto)
        r2 = await client.post(f"{BASE_URL}/admin/delivery/orders/ord-1/location", headers=headers, json={"lat": -19.227, "lng": -44.940})
        
        if r1.status_code == 200 and r2.status_code == 200:
            assert r2.json()["eta_seconds"] < r1.json()["eta_seconds"]
