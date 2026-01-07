import os
import sys
import re

def verify():
    print("🔍 [M23-25] Verificando Resiliência, Erros e Controles...")
    
    checks = [
        ("mobile/src/store/settings.store.ts", r"isSilentMode"),
        ("mobile/src/store/orders.store.ts", r"isSocketConnected"),
        ("mobile/src/screens/orders/OrdersScreen.tsx", r"offlineBanner"),
        ("mobile/src/services/orders.realtime.service.ts", r"useOrdersStore.getState\(\).setSocketStatus")
    ]
    
    errors = 0
    for path, pattern in checks:
        if not os.path.exists(path):
            print(f"❌ Arquivo ausente: {path}")
            errors += 1
            continue
        with open(path, "r", encoding="utf-8") as f:
            if not re.search(pattern, f.read()):
                print(f"❌ Lógica '{pattern}' não encontrada em {path}")
                errors += 1
            else:
                print(f"✅ {path} validado.")
    
    if errors == 0: print("✨ Missões 23, 24 e 25: OK")
    return errors == 0

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
