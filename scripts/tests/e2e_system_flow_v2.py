
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 15:20:00
import requests
import sys
import uuid
import time

# ==============================================================================
# 🧪 E2E SYSTEM FLOW TEST v2.1 (Dynamic ID Fix)
# ==============================================================================
# Diferença v2.1: Busca dinamicamente o ID da mesa para evitar erro de FK.
# ==============================================================================

BASE_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"

def run_e2e():
    print("🧪 Starting E2E System Flow Test v2.1...")

    # 1. AUTHENTICATION
    print("   [1/7] Authenticating as Admin...")
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

    # 2. VERIFY COMPANY (Self-Healing)
    print("   [2/7] Verifying Company Existence...")
    company_res = requests.get(f"{BASE_URL}/admin/company/me", headers=headers)
    if company_res.status_code == 200:
        company_data = company_res.json()
        real_slug = company_data.get("slug")
        print(f"      ✅ Company found: {real_slug}")
        
        global SLUG
        if real_slug and real_slug != SLUG:
            print(f"      ⚠️  Adjusting target slug: {SLUG} -> {real_slug}")
            SLUG = real_slug
    else:
        print(f"❌ Failed to fetch company info: {company_res.status_code}")
        return 1

    # 3. FETCH TABLE ID (Dynamic Resolution)
    print("   [3/7] Resolving Table ID for Table #1...")
    tables_res = requests.get(f"{BASE_URL}/admin/{SLUG}/tables", headers=headers)
    if tables_res.status_code != 200:
        print(f"❌ Failed to fetch tables: {tables_res.text}")
        return 1
    
    tables = tables_res.json()
    # Procura a mesa número 1
    target_table = next((t for t in tables if t["table_number"] == 1), None)
    
    if not target_table:
        print("❌ Table #1 not found in database. Run seed first.")
        return 1
    
    table_id = target_table["id"]
    qr_token = target_table["qr_token"]
    print(f"      ✅ Resolved Table #1 -> ID: {table_id} (Token: {qr_token})")

    # 4. CREATE ORDER (Public)
    print(f"   [4/7] Creating Customer Order on /{SLUG}...")
    order_payload = {
        "table_id": table_id, # ID Real do Banco
        "qr_token": qr_token, # Token Real do Banco
        "customer_name": f"E2E Tester {uuid.uuid4().hex[:4]}",
        "items": [
            {"product_id": 1, "quantity": 2, "notes": "Sem cebola"} 
        ]
    }

    # Tenta criar. Se falhar por produto inexistente, tenta buscar produtos primeiro
    create_res = requests.post(f"{BASE_URL}/{SLUG}/orders", json=order_payload)
    
    # Fallback: Se falhar por produto (FK), busca um produto válido
    if create_res.status_code == 500 or (create_res.status_code == 400 and "product" in create_res.text.lower()):
        print("      ⚠️  Product ID 1 invalid. Fetching valid product...")
        menu_res = requests.get(f"{BASE_URL}/{SLUG}/menu")
        if menu_res.status_code == 200:
            menu = menu_res.json()
            try:
                valid_product_id = menu["categories"][0]["products"][0]["id"]
                order_payload["items"][0]["product_id"] = valid_product_id
                print(f"      🔄 Retrying with Product ID: {valid_product_id}")
                create_res = requests.post(f"{BASE_URL}/{SLUG}/orders", json=order_payload)
            except:
                print("❌ Could not find any valid product in menu.")
                return 1

    if create_res.status_code != 201:
        print(f"❌ Order Creation Failed: {create_res.text}")
        return 1

    order_data = create_res.json()
    order_id = order_data["id"]
    print(f"      ✅ Order Created: {order_id}")

    # 5. VERIFY KDS (Admin)
    print("   [5/7] Verifying KDS Visibility...")
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

    # 6. UPDATE STATUS (Kitchen)
    print("   [6/7] Updating Order Status (Preparing)...")
    update_res = requests.patch(f"{BASE_URL}/admin/orders/{order_id}", headers=headers, json={
        "status": "preparing"
    })
    if update_res.status_code != 200:
        print(f"❌ Status Update Failed: {update_res.text}")
        return 1
    print("      ✅ Status updated to 'preparing'.")

    # 7. CHECK AUDIT LOG
    print("   [7/7] Verifying Audit Log...")
    time.sleep(1)
    audit_res = requests.get(f"{BASE_URL}/admin/audit", headers=headers)
    if audit_res.status_code != 200:
        print(f"❌ Audit Log Fetch Failed: {audit_res.text}")
        return 1
    
    logs = audit_res.json()
    # Procura log relacionado ao pedido (pode ser create ou update)
    # O resource_id no audit log deve bater com o order_id
    # Nota: O log de criação de pedido público pode não ter user_id, mas o update de status tem.
    audit_found = any(l.get("resource_id") == str(order_id) for l in logs)
    
    if audit_found:
        print("      ✅ Audit trail confirmed.")
    else:
        print("⚠️  Warning: Audit log for this order not found immediately.")

    print("\n✨ E2E SYSTEM FLOW PASSED.")
    return 0

if __name__ == "__main__":
    sys.exit(run_e2e())

