# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 19:05:00
import os
from pathlib import Path

# ==============================================================================
# 📚 MARKDOWN COLLECTOR (Safe Mode)
# ==============================================================================
# Varre o projeto em busca de arquivos .md e consolida em um único arquivo.
# Fix: Tags de delimitação são construídas dinamicamente para não quebrar o parser.
# ==============================================================================

OUTPUT_FILE = "todos_markdowns.txt"

IGNORE_DIRS = {
    '.git', '.vscode', '.idea', 'node_modules', 'venv', '.venv', 
    '__pycache__', '.pytest_cache', '.next', 'dist', 'build', 
    'coverage', 'android', 'ios', 'ignorar', '.expo'
}

def collect():
    print(f"📚 Iniciando coleta de arquivos Markdown (.md)...")
    
    root_path = Path(".")
    count = 0
    
    # Construção dinâmica das tags para evitar conflito com o atualizar.py
    TAG_BEGIN = "[[MESAFLOW_" + "BEGIN:"
    TAG_END = "[[MESAFLOW_" + "END]]"
    
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            out.write(f"# MESAFLOW DOCUMENTATION BUNDLE\n")
            # os.times() retorna tupla, melhor usar datetime ou string simples
            from datetime import datetime
            out.write(f"# Generated at: {datetime.now().isoformat()}\n\n")

            for root, dirs, files in os.walk(root_path):
                # Filtragem de diretórios in-place
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                
                for file in files:
                    if file.endswith(".md"):
                        file_path = Path(root) / file
                        # Normaliza caminho para forward slashes
                        rel_path = file_path.as_posix()
                        
                        try:
                            content = file_path.read_text(encoding="utf-8")
                            
                            out.write(f"{TAG_BEGIN}{rel_path}]]\n")
                            out.write(content)
                            # Garante quebra de linha no final
                            if not content.endswith("\n"):
                                out.write("\n")
                            out.write(f"{TAG_END}\n\n")
                            
                            print(f"   📄 Coletado: {rel_path}")
                            count += 1
                        except Exception as e:
                            print(f"   ❌ Erro ao ler {rel_path}: {e}")

        print("-" * 50)
        print(f"✨ Sucesso! {count} arquivos Markdown consolidados em '{OUTPUT_FILE}'.")

    except Exception as e:
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    collect()

