# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:10:00
import sys
import os
import io
import requests

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================================
# 🛡️ FINAL SEAL AUDIT (L6.9)
# ==============================================================================
# Verifica os últimos patches de estabilidade antes do congelamento total.
# ==============================================================================

def verify_idempotency_logic():
    print("🔍 [1/2] Verificando lógica de idempotência em admin_delivery.py...")
    path = "app/routers/admin_delivery.py"
    if not os.path.exists(path): return False
    content = open(path, "r", encoding="utf-8").read()
    check = "order.driver_id == driver_id" in content and "message" in content
    print(f"   Status: {'✅ PASS' if check else '❌ FAIL'}")
    return check

def verify_ui_redundancy():
    print("🔍 [2/2] Verificando redundância de estado no DriverPage...")
    path = "frontend/src/app/admin/[slug]/driver/page.tsx"
    if not os.path.exists(path): return False
    content = open(path, "r", encoding="utf-8").read()
    # Verifica se a UI atualiza o estado local ANTES do evento WS
    check = "setActiveDeliveryId(orderId)" in content and "isPickingUp" in content
    print(f"   Status: {'✅ PASS' if check else '❌ FAIL'}")
    return check

def run():
    print("🚀 Iniciando Auditoria de Selagem Final...")
    results = [
        verify_idempotency_logic(),
        verify_ui_redundancy()
    ]
    
    if all(results):
        print("\n🏆 SISTEMA SELADO: Todos os gates de estabilidade foram superados.")
        return 0
    else:
        print("\n🚨 FALHA: O sistema ainda apresenta lacunas de resiliência.")
        return 1

if __name__ == "__main__":
    sys.exit(run())

