# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:58:00
import os
from pathlib import Path

def validate():
    print("Validando TASK-ENV-01 (Environment Standardization)")
    
    # 1. Verifica .env.example
    example_path = Path(".env.example")
    if not example_path.exists():
        print("[ERRO] .env.example nao encontrado.")
        exit(1)
    
    content = example_path.read_text(encoding="utf-8")
    required_keys = ["MP_APP_ID", "STRIPE_SECRET_KEY", "WHATSAPP_INSTANCE", "AWS_BUCKET_NAME"]
    
    for key in required_keys:
        if key not in content:
            print(f"[ERRO] Chave obrigatoria {key} ausente no .env.example")
            exit(1)
    
    # 2. Verifica script de auditoria
    audit_script = Path("scripts/setup/audit_env.py")
    if not audit_script.exists():
        print("[ERRO] Script scripts/setup/audit_env.py nao encontrado.")
        exit(1)

    print("✅ TASK-ENV-01: Estrutura de ambiente validada.")
    exit(0)

if __name__ == "__main__":
    validate()
