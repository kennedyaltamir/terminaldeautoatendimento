import os
import sys

def verify():
    print("🔍 [M27] Verificando Observabilidade (Logger)...")
    
    checks = [
        ("mobile/src/services/logger.service.ts", "LoggerService"),
        ("mobile/src/services/orders.realtime.service.ts", "logger.info"),
        ("mobile/src/services/orders.sync.service.ts", "logger.error")
    ]
    
    errors = 0
    for path, content in checks:
        if not os.path.exists(path):
            print(f"❌ Arquivo ausente: {path}")
            errors += 1
            continue
        with open(path, "r", encoding="utf-8") as f:
            if content not in f.read():
                print(f"❌ Instrumentação '{content}' não encontrada em {path}")
                errors += 1
            else:
                print(f"✅ {path} validado.")
                
    if errors == 0: print("✨ Missão 27: OK")
    return errors == 0

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
