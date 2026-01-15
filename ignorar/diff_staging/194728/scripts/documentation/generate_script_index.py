import os
import re
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 📜 SCRIPT INDEX GENERATOR (Metadata Extractor)
# ==============================================================================
# Destino: docs/SCRIPT_INDEX.md
# ==============================================================================

OUTPUT_FILE = Path("docs/SCRIPT_INDEX.md")

IGNORE_DIRS = {
    '.git', '.vscode', '.idea', 'node_modules', 'venv', '.venv', 
    '__pycache__', '.pytest_cache', '.next', 'dist', 'build', 
    'coverage', 'android', 'ios', 'ignorar', '.expo', 'backups'
}

SCRIPT_EXT = {'.py', '.sh', '.bat', '.ps1', '.js', '.ts'}

def extract_metadata(path):
    """Extrai descrição de Docstrings ou comentários."""
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return "Script executável."

    # 1. Python Docstrings
    if path.suffix == '.py':
        docstring = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring:
            lines = docstring.group(1).strip().splitlines()
            for line in lines:
                if line.strip() and "DOMAIN" not in line:
                    return line.strip()

    # 2. Comentários de Cabeçalho
    for line in content.splitlines()[:15]:
        clean = line.strip()
        if not clean: continue
        
        # Ignora metadados do MesaFlow
        if "DOMAIN:" in clean or "LAST_MODIFIED:" in clean or "MESAFLOW_" in clean:
            continue
            
        # Detecta comentários
        if clean.startswith("#") or clean.startswith("//") or clean.startswith("::"):
            comment = clean.lstrip("#/: ").strip()
            if comment and not comment.startswith("="):
                return comment

    return "Sem descrição."

def generate():
    print("📜 Mapeando inventário de scripts...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    structure = {}
    root_path = Path(".")
    count = 0

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix not in SCRIPT_EXT: continue
            if file in ['__init__.py', 'next.config.js', 'tailwind.config.ts']: continue

            parent = str(Path(root).relative_to(root_path)).replace("\\", "/")
            if parent == ".": parent = "Raiz"
            
            if parent not in structure: structure[parent] = []
            
            desc = extract_metadata(file_path)
            rel_link = os.path.relpath(file_path, OUTPUT_FILE.parent).replace("\\", "/")
            
            structure[parent].append({
                "file": file,
                "desc": desc,
                "link": rel_link,
                "ext": file_path.suffix
            })
            count += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 📜 Índice de Scripts & Automação\n")
        f.write(f"> **Gerado em:** {datetime.now().isoformat()}\n")
        f.write(f"> **Total:** {count} scripts\n\n")

        for folder in sorted(structure.keys()):
            f.write(f"## 📂 `{folder}`\n")
            f.write("| Script | Tipo | Descrição |\n| :--- | :---: | :--- |\n")
            for item in sorted(structure[folder], key=lambda x: x['file']):
                icon = "🐍" if item['ext'] == '.py' else "🐚"
                f.write(f"| [{item['file']}]({item['link']}) | {icon} | {item['desc']} |\n")
            f.write("\n")

    print(f"✅ Índice gerado: {OUTPUT_FILE}")
    
    # Remove o arquivo redundante da raiz se existir
    redundant = Path("DOCUMENTATION_INDEX.md")
    if redundant.exists():
        try:
            os.remove(redundant)
            print("🗑️  Arquivo redundante 'DOCUMENTATION_INDEX.md' removido da raiz.")
        except: pass

if __name__ == "__main__":
    generate()
