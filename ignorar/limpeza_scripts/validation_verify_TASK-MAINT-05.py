# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 15:30:00
import os
from pathlib import Path

def validate():
    print("🔍 Validando TASK-MAINT-05 (Monitor Documentation & Capture)")
    
    # 1. Verificar Guia
    guide = Path("docs/manuals/PUBLIC_MONITOR_GUIDE.md")
    if not guide.exists():
        print("❌ ERRO: Guia do Monitor não encontrado.")
        exit(1)
    
    # 2. Verificar Script de Captura
    script = Path("scripts/automation/capture_monitor_screen.py")
    if not script.exists():
        print("❌ ERRO: Script de captura não encontrado.")
        exit(1)
        
    print("✅ Documentação e ferramentas de auditoria validadas.")
    exit(0)

if __name__ == "__main__":
    validate()
