
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 09:30:00
import os
import sys
from pathlib import Path

def check_syntax_noise():
    print("🔍 Verificando ruído de metadados em arquivos TypeScript...")
    mobile_src = Path("mobile/src")
    extensions = [".ts", ".tsx"]
    errors = 0

    for path in mobile_src.rglob("*"):
        if path.suffix in extensions:
            try:
                content = path.read_text(encoding="utf-8")
                lines = content.splitlines()
                # Verifica as primeiras 5 linhas por comentários de estilo Python (#)
                for i, line in enumerate(lines[:5]):
                    if line.strip().startswith("#"):
                        print(f"❌ ERRO DE SINTAXE: Ruído detectado em {path}:{i+1} -> '{line}'")
                        errors += 1
            except Exception as e:
                print(f"⚠️ Falha ao ler {path}: {e}")

    if errors > 0:
        print(f"\n🚨 Total de violações: {errors}. O build irá falhar.")
        return False
    
    print("✅ Todos os arquivos de código estão limpos.")
    return True

if __name__ == "__main__":
    if not check_syntax_noise():
        sys.exit(1)

