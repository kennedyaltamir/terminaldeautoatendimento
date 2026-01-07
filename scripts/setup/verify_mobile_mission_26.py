import os
import sys
import re

def verify():
    print("🔍 [M26] Verificando Persistência Local e Boot...")
    
    checks = [
        ("mobile/src/store/orders.store.ts", r"persist\("),
        ("mobile/src/store/orders.store.ts", r"isHydrated"),
        ("mobile/src/screens/orders/OrdersScreen.tsx", r"if \(!isHydrated\)")
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
                
    if errors == 0: print("✨ Missão 26: OK")
    return errors == 0

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
