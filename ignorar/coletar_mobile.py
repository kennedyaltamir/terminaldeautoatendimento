import os
from pathlib import Path

TARGET_DIR = "mobile"
OUTPUT_FILE = "contexto_mobile_atual.txt"
ALLOWED_EXTENSIONS = {'.ts', '.tsx', '.json'}
IGNORE_DIRS = {'node_modules', '.expo', 'build', '.venv', '__pycache__', 'android', 'ios'}

def collect_files():
    print(f"🔍 Iniciando coleta em: {TARGET_DIR}...")
    count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("<!-- MESAFLOW MOBILE CONTEXT BUNDLE -->\n")
        root_path = Path(TARGET_DIR)
        for path in root_path.rglob("*"):
            if any(ignore in path.parts for ignore in IGNORE_DIRS): continue
            if path.is_file() and path.suffix in ALLOWED_EXTENSIONS:
                rel_path = path.as_posix()
                try:
                    content = path.read_text(encoding="utf-8")
                    out.write(f"[[MESAFLOW_BEGIN:{rel_path}]]\n{content}\n[[MESAFLOW_END]]\n\n")
                    print(f"   ✅ Incluído: {rel_path}")
                    count += 1
                except Exception as e: print(f"   ❌ Erro ao ler {rel_path}: {e}")
    print(f"\n✨ Concluído! {count} arquivos em: {OUTPUT_FILE}")

if __name__ == "__main__":
    collect_files()
