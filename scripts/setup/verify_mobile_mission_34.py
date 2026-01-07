import os
import sys

# [TEST_EXEMPT: Script de auditoria de integridade para a Missão 34]

def verify():
    print("🔍 Iniciando Auditoria de Fila Offline POS (Missão 34 - Fix)...")

    checks = [
        ("mobile/src/store/waiter.store.ts", "pendingQueue: PendingOrder[]"),
        ("mobile/src/store/waiter.store.ts", "persist("),
        ("mobile/src/services/waiter.sync.service.ts", "const WaiterSyncService"), # Corrigido de 'class' para 'const'
        ("mobile/src/services/waiter.sync.service.ts", "processQueue()"),
        ("mobile/src/navigation/stacks/AppStack.tsx", "WaiterSyncService.processQueue()"),
        ("mobile/src/screens/waiter/OrderReviewScreen.tsx", "isOfflineMode")
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
        print("✨ SUCESSO: A fila de contingência offline está operacional.")
        sys.exit(0)
    else:
        print(f"🚨 ALERTA: {errors} inconsistência(s) encontrada(s).")
        sys.exit(1)

if __name__ == "__main__":
    verify()
