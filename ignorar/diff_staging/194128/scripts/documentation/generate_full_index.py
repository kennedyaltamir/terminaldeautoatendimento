import os
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🗺️ FULL DOCUMENTATION MAPPER (Canonical Fix)
# ==============================================================================
# Gera um índice clicável de TODOS os arquivos Markdown ativos no projeto.
# Destino: docs/DOCUMENTATION_INDEX.md (Compliance L6)
# ==============================================================================

OUTPUT_FILE = Path("docs/DOCUMENTATION_INDEX.md")

# Pastas para ignorar (Lixo técnico)
IGNORE_DIRS = {
    '.git', '.vscode', '.idea', 'node_modules', 'venv', '.venv', 
    '__pycache__', '.pytest_cache', '.next', 'dist', 'build', 
    'coverage', 'android', 'ios', 'ignorar', '.expo', 'backups'
}

def get_file_info(path):
    """Lê o arquivo e tenta extrair um Título e uma Descrição."""
    title = path.name
    description = "Documentação técnica."
    try:
        content = path.read_text(encoding="utf-8").splitlines()
        # 1. Tenta achar o Título (Primeira linha com #)
        for line in content:
            if line.startswith("# ") and "DOMAIN:" not in line:
                title = line.replace("# ", "").strip()
                break
        # 2. Tenta achar a Descrição (Primeira linha de texto não vazia após o título)
        for line in content:
            clean = line.strip()
            # Pula cabeçalhos, linhas vazias, comentários e tags de domínio
            if not clean or clean.startswith("#") or clean.startswith("[[") or clean.startswith("<") or clean.startswith(">"):
                continue
            description = clean
            break
    except Exception:
        pass
    return title, description

def generate():
    print("🗺️  Mapeando todo o conhecimento do projeto...")
    
    # Garante que a pasta destino existe
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    structure = {}
    root_path = Path(".")

    # 1. Varredura
    for root, dirs, files in os.walk(root_path):
        # Filtragem de diretórios
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file.endswith(".md") and file != OUTPUT_FILE.name:
                file_path = Path(root) / file
                
                # Organiza por pasta pai
                parent = str(Path(root).relative_to(root_path)).replace("\\", "/")
                if parent == ".": parent = "Raiz"
                
                if parent not in structure:
                    structure[parent] = []
                
                title, desc = get_file_info(file_path)
                
                # Link relativo (precisa ajustar pois o index agora está em docs/)
                # De docs/INDEX.md para raiz/arquivo.md -> ../arquivo.md
                rel_link = os.path.relpath(file_path, OUTPUT_FILE.parent).replace("\\", "/")
                
                structure[parent].append({
                    "file": file,
                    "title": title,
                    "desc": desc,
                    "link": rel_link
                })

    # 2. Geração do Markdown
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🗺️ Mapa Completo de Documentação MesaFlow\n")
        f.write(f"> **Gerado em:** {datetime.now().isoformat()}\n")
        f.write(f"> Este índice contém **todos** os arquivos de documentação ativos no projeto.\n\n")

        # Ordena as pastas (Raiz primeiro, depois alfabético)
        sorted_folders = sorted(structure.keys())
        if "Raiz" in sorted_folders:
            sorted_folders.remove("Raiz")
            sorted_folders.insert(0, "Raiz")

        for folder in sorted_folders:
            files = structure[folder]
            f.write(f"## 📂 {folder}\n")
            
            # Ordena arquivos por nome
            for item in sorted(files, key=lambda x: x['file']):
                # Formato: - [Nome do Arquivo](link): Descrição curta...
                f.write(f"- [**{item['file']}**]({item['link']})<br>\n")
                f.write(f"  *{item['title']}* — {item['desc']}\n\n")

    print(f"✅ Índice Completo gerado em: {OUTPUT_FILE}")
    
    # 3. Limpeza do arquivo antigo na raiz (se existir)
    old_file = Path("DOCUMENTATION_INDEX.md")
    if old_file.exists():
        try:
            os.remove(old_file)
            print("🗑️  Arquivo redundante na raiz removido.")
        except:
            pass

if __name__ == "__main__":
    generate()
