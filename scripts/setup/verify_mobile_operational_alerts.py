import os
import sys

def verify():
    print("🔍 Verificando Arquitetura de Alertas Operacionais (v2.1 - Debug Enabled)...")

    critical_files = [
        "mobile/src/services/alerts/alerts.policy.ts",
        "mobile/src/services/alerts/alerts.engine.service.ts",
        "mobile/src/services/alerts/alerts.output.service.ts",
        "mobile/src/store/orders.store.ts"
    ]

    errors = 0
    for f in critical_files:
        if not os.path.exists(f):
            print(f"❌ Arquivo ausente: {f}")
            errors += 1
        else:
            print(f"✅ Encontrado: {f}")

    # 1. Validar Pureza da Engine
    engine_path = "mobile/src/services/alerts/alerts.engine.service.ts"
    if os.path.exists(engine_path):
        with open(engine_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "AlertsOutputService" in content:
                print("❌ VIOLAÇÃO: AlertsEngineService está acoplada ao OutputService.")
                errors += 1
            else:
                print("✅ AlertsEngineService validada como função de decisão pura.")

    # 2. Validar Orquestração na Store com Log Detalhado
    store_path = "mobile/src/store/orders.store.ts"
    if os.path.exists(store_path):
        with open(store_path, "r", encoding="utf-8") as f:
            content = f.read()
            has_method = "evaluateAlerts" in content
            has_trigger = "AlertsOutputService.trigger" in content
            
            if has_method and has_trigger:
                print("✅ OrdersStore validada como orquestradora de alertas.")
            else:
                if not has_method: print("❌ FALHA: Método 'evaluateAlerts' não encontrado na Store.")
                if not has_trigger: print("❌ FALHA: Chamada 'AlertsOutputService.trigger' não encontrada na Store.")
                errors += 1

    # 3. Validar Desacoplamento do AppStack
    app_stack_path = "mobile/src/navigation/stacks/AppStack.tsx"
    if os.path.exists(app_stack_path):
        with open(app_stack_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "AlertsEngineService.process" in content:
                print("❌ VIOLAÇÃO: AppStack ainda contém lógica legada da Engine.")
                errors += 1
            else:
                print("✅ AppStack desacoplado.")

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s).")
        sys.exit(1)

    print("\n✨ Mobile operational alert architecture verified successfully.")

if __name__ == "__main__":
    verify()
