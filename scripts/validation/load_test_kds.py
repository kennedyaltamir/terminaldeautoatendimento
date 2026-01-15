
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 15:45:00
import asyncio
import httpx
import time
import sys
import random
from datetime import datetime

# ==============================================================================
# 🔥 KDS LOAD TESTER (Lightweight)
# ==============================================================================
# Simula 50 clientes enviando pedidos simultaneamente para testar:
# 1. Capacidade de escrita do Banco (Postgres).
# 2. Capacidade de broadcast do WebSocket (Redis/Memory).
# 3. Renderização do Frontend (se a aba estiver aberta).
# ==============================================================================

BASE_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"
TOTAL_ORDERS = 50
CONCURRENCY = 10  # Lotes de 10 para não travar máquina local de dev

async def create_order(client: httpx.AsyncClient, idx: int):
    """Cria um pedido único simulando um cliente."""
    payload = {
        "customer_name": f"LoadTest #{idx:03d}",
        "order_type": "takeout",
        "payment_method": "pix",
        "items": [
            {
                "product_id": 1, # Assume que o X-Bacon (ID 1) existe pelo Seed
                "quantity": random.randint(1, 3),
                "notes": f"Teste de Carga {datetime.now().strftime('%H:%M:%S')}"
            }
        ]
    }
    
    start = time.time()
    try:
        resp = await client.post(f"/{SLUG}/orders", json=payload)
        duration = time.time() - start
        return {
            "status": resp.status_code,
            "duration": duration,
            "id": resp.json().get("id") if resp.status_code == 201 else None,
            "error": None if resp.status_code == 201 else resp.text
        }
    except Exception as e:
        return {"status": 0, "duration": 0, "id": None, "error": str(e)}

async def run_load_test():
    print(f"🔥 Iniciando Teste de Carga: {TOTAL_ORDERS} pedidos em {SLUG}...")
    print("⚠️  DICA: Mantenha a aba do KDS (/admin/hamburgueria-ze/kitchen) aberta para ver o efeito Matrix!")
    
    # Pre-check de conectividade
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            await client.get("/health")
        except:
            print("❌ API Offline. Inicie o servidor com 'python run.py'.")
            return

    results = []
    start_total = time.time()

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # Divide em lotes para controle de fluxo
        for i in range(0, TOTAL_ORDERS, CONCURRENCY):
            batch = range(i, min(i + CONCURRENCY, TOTAL_ORDERS))
            print(f"   🚀 Disparando lote {i+1}-{min(i+CONCURRENCY, TOTAL_ORDERS)}...")
            
            tasks = [create_order(client, idx) for idx in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            # Pequena pausa para não saturar o SQLite/Postgres local se for muito fraco
            await asyncio.sleep(0.1)

    end_total = time.time()
    total_time = end_total - start_total
    
    # Análise
    success = [r for r in results if r["status"] == 201]
    failed = [r for r in results if r["status"] != 201]
    avg_time = sum(r["duration"] for r in success) / len(success) if success else 0
    rps = len(success) / total_time

    print("\n📊 RESULTADOS DO STRESS TEST")
    print("========================================")
    print(f"Tempo Total:      {total_time:.2f}s")
    print(f"Pedidos Criados:  {len(success)} / {TOTAL_ORDERS}")
    print(f"Taxa de Sucesso:  {(len(success)/TOTAL_ORDERS)*100:.1f}%")
    print(f"Throughput:       {rps:.2f} req/s")
    print(f"Latência Média:   {avg_time*1000:.0f}ms")
    print("========================================")

    if failed:
        print("\n❌ Erros Encontrados:")
        print(f"   - {failed[0]['error']}")
        if len(failed) > 1: print(f"   - ... e mais {len(failed)-1} erros.")
    else:
        print("\n✅ KDS LOAD TEST PASSED: O sistema aceitou a carga.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_load_test())

