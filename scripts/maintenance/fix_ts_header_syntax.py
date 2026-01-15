import os
from pathlib import Path

# ==============================================================================
# 🔧 TS/TSX HEADER SYNTAX FIXER
# ==============================================================================
# Varre arquivos .ts e .tsx e corrige comentários de metadados que usam '#'
# para a sintaxe correta '//'.
# ==============================================================================

TARGET_DIR = Path("frontend/src")

def fix_headers():
    print("🔧 Iniciando correção de sintaxe de headers em arquivos TS/TSX...")
    count = 0
    
    for path in TARGET_DIR.rglob("*"):
        if path.suffix not in ['.ts', '.tsx']:
            continue
            
        try:
            content = path.read_text(encoding="utf-8")
            new_lines = []
            modified = False
            
            for line in content.splitlines():
                # Detecta linhas de metadados com sintaxe errada
                if line.startswith("# DOMAIN:") or line.startswith("# LAST_MODIFIED:"):
                    new_line = line.replace("# ", "// ")
                    new_lines.append(new_line)
                    modified = True
                else:
                    new_lines.append(line)
            
            if modified:
                # Reconstrói o arquivo com quebras de linha originais (LF)
                path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                print(f"   ✅ Corrigido: {path}")
                count += 1
                
        except Exception as e:
            print(f"   ❌ Erro ao processar {path}: {e}")

    print(f"\n✨ Correção concluída. {count} arquivos ajustados.")

if __name__ == "__main__":
    fix_headers()

