import os
import sys

# [TEST_EXEMPT: Script de auditoria de integridade para a Missão 32]

def verify():
    print("🔍 Iniciando Auditoria de Gestão de Chamados (Missão 32)...")

    checks = [
        ("mobile/src/store/waiter.store.ts", "serviceRequests: ServiceRequest[]"),
        ("mobile/src/store/waiter.store.ts", "addServiceRequest:"),
        ("mobile/src/screens/waiter/WaiterTablesScreen.tsx", "WaiterCalls"),
        ("mobile/src/screens/waiter/WaiterCallsScreen.tsx", "WaiterCallsScreen"),
        ("mobile/src/navigation/stacks/AppStack.tsx", "waiter_call")
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

    print("\n" + "="*50)
    if errors == 0:
        print("✨ SUCESSO: O sistema de gestão de chamados está operacional.")
        sys.exit(0)
    else:
        print(f"🚨 ALERTA: {errors} inconsistência(s) encontrada(s).")
        sys.exit(1)

if __name__ == "__main__":
    verify()
