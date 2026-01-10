# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 01:20:00
import os
import re
from pathlib import Path

def sanitize_file_content(file_path):
    """
    Remove indentação acidental de declarações de import/export no topo do arquivo.
    """
    content = file_path.read_text(encoding="utf-8")
    
    # Regex para encontrar import/export com espaços no início da linha
    # e remover esses espaços.
    new_content = re.sub(r'^[ \t]+(import|export)\s', r'\1 ', content, flags=re.MULTILINE)
    
    if content != new_content:
        print(f"✨ Sanitizado: {file_path}")
        file_path.write_text(new_content, encoding="utf-8")
        return True
    return False

def run_fix():
    print("🧹 Iniciando sanitização de módulos mobile")
    mobile_src = Path("mobile/src")
    
    if not mobile_src.exists():
        print("❌ Pasta mobile/src nao encontrada.")
        return

    count = 0
    for file_path in mobile_src.rglob("*.ts*"):
        if sanitize_file_content(file_path):
            count += 1

    print(f"\n✅ Processo concluído. {count} arquivos foram corrigidos.")

if __name__ == "__main__":
    run_fix()
