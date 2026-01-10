import os
import sys

def verify():
    print("🔍 [M30A] Verificando Encoder ESC/POS...")
    
    checks = [
        ("mobile/src/lib/escpos.encoder.ts", "class EscPosEncoder"),
        ("mobile/src/lib/escpos.encoder.ts", "getBuffer(): Uint8Array"),
        ("mobile/src/services/printer.service.ts", "generateOrderReceipt")
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
                
    if errors == 0: print("✨ Missão 30A: OK")
    return errors == 0

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
