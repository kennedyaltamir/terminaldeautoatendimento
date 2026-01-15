# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:35:00
import os
import io
import sys
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================================
# 🗺️ FULL DOCUMENTATION MAPPER (L6 Enhanced)
# ==============================================================================

OUTPUT_FILE = Path("docs/DOCUMENTATION_INDEX.md")
IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.venv', '__pycache__', '.next', 'ignorar', 'backups'}

def get_file_summary(path):
    """Extrai o título e o primeiro parágrafo de explicação."""
    try:
        content = path.read_text(encoding="utf-8").splitlines()
        title = path.name
        summary = "Documentação técnica."
        
        found_title = False
        for line in content:
            clean = line.strip()
            if not clean or clean.startswith("DOMAIN:") or clean.startswith("LAST_MODIFIED:"):
                continue
            if clean.startswith("# ") and not found_title:
                title = clean.replace("# ", "").strip()
                found_title = True
                continue
            if found_title and clean and not clean.startswith("#") and not clean.startswith(">"):
                summary = clean
                break
        return title, summary
    except:
        return path.name, "Erro ao ler arquivo."

def generate():
    print("🗺️  Mapeando documentação com resumos...")
    structure = {}
    root_path = Path(".")

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith(".md") and file != "DOCUMENTATION_INDEX.md":
                file_path = Path(root) / file
                parent = str(Path(root).relative_to(root_path)).replace("\\", "/")
                if parent == ".": parent = "Raiz"
                if parent not in structure: structure[parent] = []
                
                title, summary = get_file_summary(file_path)
                rel_link = os.path.relpath(file_path, OUTPUT_FILE.parent).replace("\\", "/")
                
                structure[parent].append({
                    "file": file,
                    "title": title,
                    "summary": summary,
                    "link": rel_link
                })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🗺️ Mapa Completo de Documentação MesaFlow\n")
        f.write(f"> **Gerado em:** {datetime.now().isoformat()}\n\n")
        
        for folder in sorted(structure.keys()):
            f.write(f"## 📂 {folder}\n")
            for item in sorted(structure[folder], key=lambda x: x['file']):
                f.write(f"### [**{item['title']}**]({item['link']})\n")
                f.write(f"{item['summary']}\n\n")

    print(f"✅ Índice gerado em: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
