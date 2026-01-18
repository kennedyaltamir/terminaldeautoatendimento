
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 04:40:00
import os
import sys
from pathlib import Path

def audit_l4():
    app_file = Path("mobile/App.tsx")
    boundary_import = "ErrorBoundary"
    
    print("🔍 Auditando Maturidade L4 (Confiabilidade)...")
    
    if not app_file.exists():
        print("❌ FAIL: App.tsx não encontrado.")
        return False
        
    content = app_file.read_text()
    if boundary_import not in content:
        print(f"🚨 BLOQUEIO SRE: {boundary_import} não detectado no App.tsx. Risco de crash de renderização.")
        return False
        
    print("✅ SRE L4: Barreira de erro detectada.")
    return True

if __name__ == "__main__":
    if not audit_l4(): sys.exit(1)

