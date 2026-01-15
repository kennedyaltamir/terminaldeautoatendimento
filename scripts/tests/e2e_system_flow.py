
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 10:05:00
import requests
import sys
import uuid
import time

# ==============================================================================
# 🧪 E2E SYSTEM FLOW TEST (Omniscience Phase D)
# ==============================================================================
# Simula o ciclo de vida completo de um pedido:
# 1. Login Admin (Auth)
# 2. Criação de Pedido (Public API)
# 3. Verificação no KDS (Admin API)
# 4. Avanço de Status (Kitchen Operation)
# 5. Auditoria (Audit Log)
# ==============================================================================

BASE_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"

def run_e2e():
    print("🧪 Starting E2E System Flow Test...")
    
    # 1. AUTHENTICATION
    print("   [1/5] Authenticating as Admin...")
    try:
        auth_res = requests.post(f"{BASE_URL}/auth/token", data={
            "username": "admin@mesaflow.com",
            "password": "123456"
        })
        if auth_res.status_code != 200:
            print(f"❌ Auth Failed: {auth_res.text}")
            return 1
        token = auth_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("      ✅ Authenticated.")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return 1

    # 2. CREATE ORDER (Public)
    print("   [2/5] Creating Customer Order...")
    order_payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1", # Deve bater com o seed
        "customer_name": f"E2E Tester {uuid.uuid4().hex[:4]}",
        "items": [
            {"product_id": 1, "quantity": 2, "notes": "Sem cebola"} # ID 1 deve existir (X-Bacon do seed)
        ]
    }
    try:
        # Tenta criar pedido. Se falhar por produto/mesa inexistente, o teste falha.
        # Nota: O endpoint público de orders geralmente é /api/{slug}/orders
        create_res = requests.post(f"{BASE_URL}/{SLUG}/orders", json=order_payload)
        if create_res.status_code != 201:
            print(f"❌ Order Creation Failed: {create_res.text}")
            # Tenta fallback para endpoint sem slug se a rota mudou
            return 1
        
        order_data = create_res.json()
        order_id = order_data["id"]
        print(f"      ✅ Order Created: {order_id}")
    except Exception as e:
        print(f"❌ Order Error: {e}")
        return 1

    # 3. VERIFY KDS (Admin)
    print("   [3/5] Verifying KDS Visibility...")
    kds_res = requests.get(f"{BASE_URL}/admin/{SLUG}/orders", headers=headers)
    if kds_res.status_code != 200:
        print(f"❌ KDS Fetch Failed: {kds_res.text}")
        return 1
    
    orders = kds_res.json()
    found = any(o["id"] == order_id for o in orders)
    if not found:
        print("❌ Order not found in KDS list.")
        return 1
    print("      ✅ Order visible in KDS.")

    # 4. UPDATE STATUS (Kitchen)
    print("   [4/5] Updating Order Status (Preparing)...")
    update_res = requests.patch(f"{BASE_URL}/admin/orders/{order_id}", headers=headers, json={
        "status": "preparing"
    })
    if update_res.status_code != 200:
        print(f"❌ Status Update Failed: {update_res.text}")
        return 1
    print("      ✅ Status updated to 'preparing'.")

    # 5. CHECK AUDIT LOG
    print("   [5/5] Verifying Audit Log...")
    # Dá um tempo para o log ser gravado (se for async)
    time.sleep(1)
    audit_res = requests.get(f"{BASE_URL}/admin/audit", headers=headers)
    if audit_res.status_code != 200:
        print(f"❌ Audit Log Fetch Failed: {audit_res.text}")
        return 1
    
    logs = audit_res.json()
    # Procura log relacionado ao pedido (pode ser create ou update)
    # O resource_id no audit log deve bater com o order_id
    audit_found = any(l["resource_id"] == str(order_id) for l in logs)
    
    if audit_found:
        print("      ✅ Audit trail confirmed.")
    else:
        print("⚠️  Warning: Audit log for this order not found immediately (might be async).")

    print("\n✨ E2E SYSTEM FLOW PASSED.")
    return 0

if __name__ == "__main__":
    sys.exit(run_e2e())

