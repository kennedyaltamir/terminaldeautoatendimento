
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 05:50:00
import sys
import os
from pathlib import Path

# Adiciona a raiz ao path
sys.path.append(os.getcwd())

def verify_ai_readiness():
    print("🧠 Verificando Prontidão para IA (TASK-AI-01)...")
    
    # 1. Verificar dependências
    reqs = Path("requirements.txt").read_text()
    deps = ["scikit-learn", "pandas", "numpy"]
    for d in deps:
        if d in reqs:
            print(f"   ✅ Dependência {d}: OK")
        else:
            print(f"   ❌ Dependência {d}: AUSENTE")
            return False
            
    # 2. Verificar existência dos arquivos core de IA
    files = [
        "app/services/ai_prediction_service.py",
        "app/routers/admin_ai.py"
    ]
    for f in files:
        if Path(f).exists():
            print(f"   ✅ Arquivo {f}: OK")
        else:
            print(f"   ❌ Arquivo {f}: AUSENTE")
            return False
            
    print("\n✨ Sistema pronto para ativação do motor preditivo.")
    return True

if __name__ == "__main__":
    if not verify_ai_readiness():
        sys.exit(1)

