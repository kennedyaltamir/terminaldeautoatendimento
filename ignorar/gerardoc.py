import os
import re
from pathlib import Path
from datetime import datetime, timezone

# ==============================================================================
# CONFIGURAÇÃO DO GERADOR DE DOCUMENTAÇÃO (DocGen v2.4 - Clean)
# ==============================================================================

OUTPUT_FILE = "documentacao_completa.txt"
DOCS_DIR = "docs"
ROOT_FILES = ["README.md", "CONTRIBUTING.md", "LICENSE", "ROADMAP.md", "TASKS.md"]

TAG_START = "[[" + "MESAFLOW_BEGIN:"
TAG_END = "[[" + "MESAFLOW_END]]"

DOC_EXTENSIONS = {".md", ".xml", ".txt"}

IGNORE_FILES = {
    "todososarquivos.txt", 
    "documentacao_completa.txt", 
    "resposta.txt", 
    ".env.example"
    "ignorar"}

PRIORITY_ORDER = [
    "docs/governance/AI_STARTUP_SEQUENCE.xml",
    "docs/governance/README.md",
    "docs/governance/AI_ROLE_PROTOCOL.md",
    "docs/governance/FAIL_FAST_PROTOCOL.md",
    "docs/governance/UPDATE_EXECUTION_PROTOCOL.md",
    "docs/governance/ERROR_RESPONSE_MAPPING_PROTOCOL.md",
    "docs/ROADMAP.md",
    "docs/TASKS.md",
    "docs/MASTER_PROJECT_BIBLE.md"
    ]

def get_file_metadata(path_obj: Path) -> str:
    try:
        mtime = path_obj.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "UNKNOWN"

def main():
    print(f"📚 Gerando Bundle de Documentação (v2.4)...")
    
    root = Path(".")
    files = []
    
    # Coleta arquivos raiz
    for f_name in ROOT_FILES:
        p = root / f_name
        if p.exists(): files.append(p)

    # Coleta pasta docs (ignorando lixo)
    if (root / DOCS_DIR).exists():
        for p in (root / DOCS_DIR).rglob("*"):
            if p.is_file() and p.suffix.lower() in DOC_EXTENSIONS:
                if p.name not in IGNORE_FILES and "ignorar" not in p.parts:
                    files.append(p)

    # Ordenação
    def sort_key(p):
        path_str = str(p).replace("\\", "/")
        if path_str in PRIORITY_ORDER:
            return (0, PRIORITY_ORDER.index(path_str))
        return (1, path_str)
    
    files.sort(key=sort_key)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("<!-- MESAFLOW DOCUMENTATION BUNDLE -->\n\n")
        
        for p in files:
            try:
                rel_path = str(p).replace("\\", "/")
                last_mod = get_file_metadata(p)
                content = p.read_text(encoding="utf-8", errors="ignore")
                
                out.write(f"{TAG_START}{rel_path}]]\n")
                out.write(f"# LAST_MODIFIED: {last_mod}\n")
                out.write(content)
                if not content.endswith("\n"): out.write("\n")
                out.write(f"{TAG_END}\n\n")
                print(f"   ✅ {rel_path}")
            except Exception as e:
                print(f"   ❌ Erro em {rel_path}: {e}")

    print(f"✨ Documentação consolidada em: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()