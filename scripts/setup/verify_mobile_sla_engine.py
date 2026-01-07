import os
import sys

def verify():
    print("🔍 Verificando SLA Engine e Global Clock (v1.0)...")

    critical_files = [
        "mobile/src/services/global.clock.service.ts",
        "mobile/src/services/orders.sla.service.ts",
        "mobile/src/store/orders.store.ts",
        "docs/mobile/tasks/mobile_21_sla_engine.md"
    ]

    errors = 0
    for f in critical_files:
        if not os.path.exists(f):
            print(f"❌ Arquivo ausente: {f}")
            errors += 1
        else:
            print(f"✅ Encontrado: {f}")

    # 1. Validar ausência de cálculos temporais na UI
    screen_path = "mobile/src/screens/orders/OrdersScreen.tsx"
    if os.path.exists(screen_path):
        with open(screen_path, "r", encoding="utf-8") as f:
            content = f.read()
            forbidden = ["Date.now()", "new Date()", "calculateElapsedMinutes"]
            for term in forbidden:
                if term in content:
                    print(f"❌ VIOLAÇÃO: Cálculo temporal '{term}' detectado na Screen.")
                    errors += 1
            
            if "item.remainingTime" in content and "item.slaStatus" in content:
                print("✅ Consumo de estado derivado validado na UI.")
            else:
                print("❌ VIOLAÇÃO: UI não está consumindo os campos de SLA da Store.")
                errors += 1

    # 2. Validar assinatura do Clock na Store
    store_path = "mobile/src/store/orders.store.ts"
    if os.path.exists(store_path):
        with open(store_path, "r", encoding="utf-8") as f:
            if "updateSLAs" in f.read():
                print("✅ Ação de atualização de SLA encontrada na Store.")
            else:
                print("❌ VIOLAÇÃO: Store não possui lógica de atualização de SLA.")
                errors += 1

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s).")
        sys.exit(1)

    print("\n✨ Mobile KDS SLA Engine architecture verified successfully.")

if __name__ == "__main__":
    verify()
