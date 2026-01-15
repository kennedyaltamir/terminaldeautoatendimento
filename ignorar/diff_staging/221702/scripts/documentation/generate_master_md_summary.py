# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 22:15:00
import os
import io
import sys
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================================
# 📚 MASTER MD SUMMARY GENERATOR (Narrative Edition)
# ==============================================================================
# Varre todos os .md e extrai um parágrafo explicativo de cada um.
# Destino: docs/MASTER_MD_SUMMARY.md
# ==============================================================================

OUTPUT_FILE = Path("docs/MASTER_MD_SUMMARY.md")
IGNORE_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', '__pycache__', '.next', 
    'ignorar', 'backups', '.pytest_cache', 'test-results', 'playwright-report'
}

def extract_paragraph(path):
    """Extrai o primeiro parágrafo significativo após o título."""
    try:
        content = path.read_text(encoding="utf-8").splitlines()
        found_start = False
        paragraph = []
        
        for line in content:
            clean = line.strip()
            # Pula metadados e tags de sistema
            if not clean or any(x in clean for x in ["DOMAIN:", "LAST_MODIFIED:", "MESAFLOW_", "import "]):
                continue
            # Detecta o início após o título principal
            if clean.startswith("# "):
                found_start = True
                continue
            # Se já achamos o título, o próximo bloco de texto é o parágrafo
            if found_start:
                if clean.startswith(("#", ">", "[[", "-", "*", "![", "[", "```")):
                    if paragraph: break # Já pegamos o texto e chegamos em outro elemento
                    continue
                paragraph.append(clean)
                if len(paragraph) >= 2: break # Limita o tamanho do parágrafo
        
        return " ".join(paragraph) if paragraph else "Documentação técnica de suporte ao módulo."
    except:
        return "Erro ao processar descrição."

def generate():
    print("📚 Gerando Resumo Narrativo de toda a documentação...")
    md_files = []
    root_path = Path(".")

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith(".md") and file != OUTPUT_FILE.name:
                file_path = Path(root) / file
                md_files.append(file_path)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 📖 Resumo Narrativo da Documentação MesaFlow\n")
        f.write(f"> **Gerado em:** {datetime.now().isoformat()}\n")
        f.write(f"> **Escopo:** {len(md_files)} documentos analisados.\n\n")
        
        # Agrupa por diretório para organização
        current_dir = ""
        for path in sorted(md_files):
            parent = str(path.parent).replace("\\", "/")
            if parent != current_dir:
                current_dir = parent
                f.write(f"\n## 📂 Diretorio: `{current_dir}`\n\n")
            
            summary = extract_paragraph(path)
            f.write(f"### 📄 {path.name}\n")
            f.write(f"{summary}\n\n")
            f.write(f"--- \n")

    print(f"✅ Resumo Mestre gerado em: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
