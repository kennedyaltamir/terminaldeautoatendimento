import os
import sys

def verify():
    print("🔍 [M30B] Verificando Integração Bluetooth...")
    
    checks = [
        ("mobile/src/services/bluetooth.service.ts", "scanDevices"),
        ("mobile/src/store/settings.store.ts", "selectedPrinter"),
        ("mobile/src/services/printer.service.ts", "bluetoothService.connect")
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
                
    if errors == 0: print("✨ Missão 30B: OK")
    return errors == 0

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
