# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 23:20:00
import sys, io, os
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv(override=True)

def verify():
    print("🔍 Verificando Integridade do Hub iFood...")
    
    files = [
        "app/services/ifood_service.py",
        "app/routers/webhooks_ifood.py",
        "docs/manuals/IFOOD_SETUP_GUIDE.md"
    ]
    
    all_ok = True
    for f in files:
        if Path(f).exists():
            print(f"   ✅ Arquivo presente: {f}")
        else:
            print(f"   ❌ Arquivo ausente: {f}")
            all_ok = False
            
    if not os.getenv("IFOOD_CLIENT_ID"):
        print("⚠️  Aviso: IFOOD_CLIENT_ID não configurado no .env.")
        
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(verify())

