import os
import sys

def verify():
    print("🔍 [M29B] Verificando Lançamento de Itens (Carrinho)...")
    
    checks = [
        ("mobile/src/store/waiter.store.ts", "cart: CartItem[]"),
        ("mobile/src/store/waiter.store.ts", "addToCart"),
        ("mobile/src/screens/waiter/OrderEntryScreen.tsx", "renderProduct")
    ]
    
    errors = 0
    for path, content in checks:
        if not os.path.exists(path):
            print(f"❌ Arquivo ausente: {path}")
            errors += 1
            continue
        with open(path, "r", encoding="utf-8") as f:
            if content not in f.read():
                print(f"❌ Lógica '{content}' não encontrada em {path}")
                errors += 1
            else:
                print(f"✅ {path} validado.")
                
    if errors == 0: print("✨ Missão 29B: OK")
    return errors == 0

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
