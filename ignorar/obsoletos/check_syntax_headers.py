# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 01:30:00
import os
from pathlib import Path

def check():
    print("🔍 Verificando integridade de comentarios de metadados")
    frontend_dir = Path("frontend/src")
    errors = 0

    for file_path in frontend_dir.rglob("*"):
        if file_path.suffix in [".ts", ".tsx"]:
            try:
                content = file_path.read_text(encoding="utf-8")
                lines = content.splitlines()
                if lines and lines[0].startswith("# DOMAIN"):
                    print(f"❌ Erro de Sintaxe detectado em: {file_path}")
                    print(f"   Linha 1: {lines[0]}")
                    errors += 1
            except:
                continue

    if errors == 0:
        print("✅ Todos os arquivos frontend usam sintaxe de comentario correta.")
    else:
        print(f"🚨 Total de {errors} arquivos com erro de sintaxe encontrados.")

if __name__ == "__main__":
    check()
