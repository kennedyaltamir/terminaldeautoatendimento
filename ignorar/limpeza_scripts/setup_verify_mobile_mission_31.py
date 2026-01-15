import os
import sys

def verify():
    print("🔍 [M31] Verificando Push Notifications...")
    
    checks = [
        ("mobile/src/services/notifications.service.ts", "registerForPushNotifications"),
        ("mobile/src/store/auth.store.ts", "setupNotifications"),
        ("mobile/package.json", "expo-notifications")
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
                
    if errors == 0: print("✨ Missão 31: OK")
    return errors == 0

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
