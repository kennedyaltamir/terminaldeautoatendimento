# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 01:18:00
import os
import re
from pathlib import Path

def check_nested_exports():
    print("🔍 Verificando arquivos mobile em busca de 'exports' aninhados")
    mobile_src = Path("mobile/src")
    
    if not mobile_src.exists():
        print("❌ Pasta mobile/src nao encontrada.")
        return

    error_found = False
    # Regex para encontrar export que nao esteja no inicio da linha (simplificado)
    # Procura por export precedido por espacos ou dentro de chaves
    pattern = re.compile(r'^\s+export\s+', re.MULTILINE)

    for file_path in mobile_src.rglob("*.ts*"):
        content = file_path.read_text(encoding="utf-8")
        matches = pattern.findall(content)
        if matches:
            print(f"⚠️  Possivel export aninhado em: {file_path}")
            error_found = True

    if not error_found:
        print("✅ Nenhum export aninhado obvio encontrado no codigo fonte.")
    else:
        print("❌ Foram detectados padroes de exportacao suspeitos.")

if __name__ == "__main__":
    check_nested_exports()
