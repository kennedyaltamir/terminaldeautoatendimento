import os
import sys
import re

def verify():
    print("🔍 Verificando Arquitetura Realtime Mobile (v1.0)...")

    critical_files = [
        "mobile/src/services/orders.realtime.service.ts",
        "mobile/src/store/orders.store.ts",
        "mobile/src/navigation/stacks/AppStack.tsx",
        "docs/mobile/tasks/mobile_18_realtime_kds.md"
    ]

    errors = 0
    for f in critical_files:
        if not os.path.exists(f):
            print(f"❌ Arquivo ausente: {f}")
            errors += 1
        else:
            print(f"✅ Encontrado: {f}")

    # 1. Validar Isolamento da UI (OrdersScreen não pode ter WebSocket ou setInterval)
    screen_path = "mobile/src/screens/orders/OrdersScreen.tsx"
    if os.path.exists(screen_path):
        with open(screen_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "WebSocket" in content or "setInterval" in content or "OrdersRealtimeService" in content:
                print(f"❌ VIOLAÇÃO: OrdersScreen possui acoplamento com infra realtime ou timers.")
                errors += 1
            else:
                print("✅ Isolamento da UI validado.")

    # 2. Validar Lógica de Conexão na Store (Proibido)
    store_path = "mobile/src/store/orders.store.ts"
    if os.path.exists(store_path):
        with open(store_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "new WebSocket" in content:
                print(f"❌ VIOLAÇÃO: OrdersStore está criando conexões de rede diretamente.")
                errors += 1
            else:
                print("✅ Pureza da Store validada.")

    # 3. Validar Orquestração na AppStack
    app_stack_path = "mobile/src/navigation/stacks/AppStack.tsx"
    if os.path.exists(app_stack_path):
        with open(app_stack_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "OrdersRealtimeService.connect" in content and "OrdersRealtimeService.disconnect" in content:
                print("✅ Orquestração de conexão na AppStack validada.")
            else:
                print(f"❌ VIOLAÇÃO: AppStack não está gerenciando o ciclo de vida da conexão.")
                errors += 1

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s).")
        sys.exit(1)

    print("\n✨ Mobile KDS Realtime architecture verified successfully.")

if __name__ == "__main__":
    verify()
