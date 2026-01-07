import os
import sys

def verify():
    print("🔍 Verificando Identidade Operacional Mobile (v1.1 - Hardened)...")

    checks = [
        ("mobile/src/store/session.store.ts", "initializeSession"),
        ("mobile/src/types/realtime.events.ts", "export type RealtimeEvent"),
        ("mobile/src/navigation/stacks/AppStack.tsx", "authStatus === 'authenticated'")
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

    # Validação de Dependência Circular (Bug Fix Turno Anterior)
    ws_service_path = "mobile/src/services/orders.realtime.service.ts"
    if os.path.exists(ws_service_path):
        with open(ws_service_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "import { RealtimeEvent } from './orders.realtime.service'" in content:
                print("❌ VIOLAÇÃO: Dependência circular detectada no WebSocket Service.")
                errors += 1
            elif "import { RealtimeEvent } from '../types/realtime.events'" in content:
                print("✅ Centralização de tipos validada.")

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s).")
        sys.exit(1)

    print("\n✨ Mobile operational identity bootstrap verified successfully.")

if __name__ == "__main__":
    verify()
