# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 22:15:00
import os
import re
import sys
import io
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================================
# 📜 SCRIPT INDEX GENERATOR v2.0 (Strict Mode)
# ==============================================================================
# Filtra apenas ferramentas de manutenção e validação.
# Ignora código-fonte do produto (src/, app/).
# ==============================================================================

OUTPUT_FILE = Path("docs/SCRIPT_INDEX.md")

# Pastas que REALMENTE contêm scripts de automação
ALLOWED_SCRIPT_ROOTS = ["scripts", "comunication/scripts"]
# Arquivos na raiz que são ferramentas
ALLOWED_ROOT_FILES = ["atualizar.py", "gerartxt.py", "run.py", "dev.bat"]

IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.venv', '__pycache__', '.next', 'ignorar', 'backups', 'src', 'app'}
SCRIPT_EXT = {'.py', '.sh', '.bat', '.ps1'}

def extract_metadata(path):
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        # Tenta Docstring
        docstring = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring:
            lines = docstring.group(1).strip().splitlines()
            for line in lines:
                if line.strip() and "DOMAIN" not in line: return line.strip()
        # Tenta Comentário de topo
        for line in content.splitlines()[:10]:
            clean = line.strip()
            if not clean or any(x in clean for x in ["DOMAIN:", "LAST_MODIFIED:", "MESAFLOW_"]): continue
            if clean.startswith(("#", "//", "::")):
                comment = clean.lstrip("#/: ").strip()
                if comment and not comment.startswith("="): return comment
    except: pass
    return "Script de automação."

def generate():
    print("📜 Gerando Índice de Scripts Estrito...")
    structure = {}
    count = 0

    # 1. Varre pastas permitidas
    for root_name in ALLOWED_SCRIPT_ROOTS:
        root_path = Path(root_name)
        if not root_path.exists(): continue
        
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix not in SCRIPT_EXT: continue
                
                parent = str(file_path.parent).replace("\\", "/")
                if parent not in structure: structure[parent] = []
                
                structure[parent].append({
                    "file": file,
                    "desc": extract_metadata(file_path),
                    "link": os.path.relpath(file_path, OUTPUT_FILE.parent).replace("\\", "/"),
                    "ext": file_path.suffix
                })
                count += 1

    # 2. Adiciona arquivos da raiz
    structure["Raiz"] = []
    for f_name in ALLOWED_ROOT_FILES:
        f_path = Path(f_name)
        if f_path.exists():
            structure["Raiz"].append({
                "file": f_name,
                "desc": extract_metadata(f_path),
                "link": os.path.relpath(f_path, OUTPUT_FILE.parent).replace("\\", "/"),
                "ext": f_path.suffix
            })
            count += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 📜 Índice de Scripts & Automação\n")
        f.write(f"> **Gerado em:** {datetime.now().isoformat()}\n")
        f.write(f"> **Total:** {count} ferramentas de manutenção\n\n")
        
        for folder in sorted(structure.keys()):
            if not structure[folder]: continue
            f.write(f"## 📂 `{folder}`\n")
            f.write("| Script | Tipo | Descrição |\n| :--- | :---: | :--- |\n")
            for item in sorted(structure[folder], key=lambda x: x['file']):
                icon = "🐍" if item['ext'] == '.py' else "🐚"
                f.write(f"| [{item['file']}]({item['link']}) | {icon} | {item['desc']} |\n")
            f.write("\n")

    print(f"✅ SCRIPT_INDEX atualizado: {count} itens.")

if __name__ == "__main__":
    generate()

