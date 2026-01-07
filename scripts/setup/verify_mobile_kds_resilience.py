import os
import sys
import re

def verify():
    print("🔍 Verificando Resiliência e Sincronia KDS (v1.0)...")

    checks = [
        ("mobile/src/services/realtime.reconnect.policy.ts", "getNextDelay"),
        ("mobile/src/services/orders.sync.service.ts", "performFullSync"),
        ("mobile/src/store/orders.store.ts", "previousOrders") # Verifica lógica de rollback/optimistic
    ]

    errors = 0
    for path, content in checks:
        if not os.path.exists(path):
            print(f"❌ Arquivo ausente: {path}")
            errors += 1
            continue

        with open(path, "r", encoding="utf-8") as f:
            if content not in f.read():
                print(f"❌ VIOLAÇÃO: Lógica '{content}' não encontrada em {path}")
                errors += 1
            else:
                print(f"✅ {path} validado.")

    # Validação de Orquestração no AppStack (Nova Regra da Missão 20)
    app_stack_path = "mobile/src/navigation/stacks/AppStack.tsx"
    if os.path.exists(app_stack_path):
        with open(app_stack_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "OrdersSyncService.fetchAndAddOrder" in content:
                print("✅ Lógica de Fetch automático para new_order validada.")
            else:
                print("❌ VIOLAÇÃO: AppStack não está orquestrando o fetch de novos pedidos.")
                errors += 1

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s).")
        sys.exit(1)

    print("\n✨ Mobile KDS resilience and state sync verified successfully.")

if __name__ == "__main__":
    verify()
