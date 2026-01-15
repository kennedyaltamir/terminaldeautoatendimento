# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 03:00:00
import os
from pathlib import Path

def validate():
    print("🔍 Validando TASK-MAINT-04 (Mobile Screenshots)")
    
    output_dir = Path("docs/screenshots/mobile")
    if not output_dir.exists():
        print("❌ ERRO: Pasta de screenshots mobile nao encontrada.")
        exit(1)
        
    files = list(output_dir.glob("*.png"))
    if len(files) == 0:
        print("❌ ERRO: Nenhuma captura de tela mobile encontrada.")
        exit(1)
        
    print(f"✅ Sucesso: {len(files)} capturas de tela mobile detectadas.")
    exit(0)

if __name__ == "__main__":
    validate()
