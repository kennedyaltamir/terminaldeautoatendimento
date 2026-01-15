
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 04:30:00
import os
import sys
from pathlib import Path

def audit():
    mobile_src = Path("mobile/src")
    forbidden_patterns = ["MOCK_", "192.168.", "localhost", "fake-token"]
    errors = 0

    print("🔍 Verificando integridade de produção em /mobile/src...")
    
    for path in mobile_src.rglob("*.tsx"):
        if "node_modules" in str(path): continue
        content = path.read_text()
        for pattern in forbidden_patterns:
            if pattern in content:
                # Exceção para env.ts que tem fallback de dev
                if "env.ts" in path.name and pattern in ["192.168.", "localhost"]:
                    continue
                print(f"  [ERROR] Padrão proibido '{pattern}' encontrado em: {path}")
                errors += 1

    if errors > 0:
        print(f"\n❌ AUDITORIA FALHOU: {errors} violações de produção encontradas.")
        sys.exit(1)
    
    print("✅ AUDITORIA PASSOU: Nenhum mock ou IP local detectado nas telas.")
    sys.exit(0)

if __name__ == "__main__":
    audit()

