# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 02:40:00
import os
from pathlib import Path

def validate():
    print("🔍 Validando TASK-MAINT-03 (Visual Audit)")
    
    output_dir = Path("docs/screenshots")
    if not output_dir.exists():
        print("❌ ERRO: Pasta de screenshots nao encontrada.")
        exit(1)
        
    files = list(output_dir.glob("*.png"))
    if len(files) < 10:
        print(f"❌ ERRO: Poucas capturas geradas ({len(files)}). Esperado > 10.")
        exit(1)
        
    print(f"✅ Sucesso: {len(files)} capturas de tela encontradas.")
    exit(0)

if __name__ == "__main__":
    validate()
