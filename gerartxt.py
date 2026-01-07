import os
import shutil
from pathlib import Path
import hashlib
from datetime import datetime, timezone

# ==============================================================================
# CONFIGURAÇÃO DE GOVERNANÇA DE CONTEXTO (v9.3)
# ==============================================================================

OUTPUT_FILE = "todososarquivos.txt"
TRASH_FOLDER = "ignorar"

# 1. ARQUIVOS PARA MOVER PARA 'ignorar/' (Lixo/Obsoletos)
TRASH_PATTERNS = [
    "HANDOVER_MESAFLOW",
    "docs/Prompts/Pedir para transferir.txt",
    "docs/Prompts/Promptcorrigirsysteminstructions.txt",
    "docs/Prompts/Prompttransferencia1.txt",
    "dummy.txt",
    "path",
    "state.status)",
    "state.slug)",
    "atualizar.log"
]

# 2. PASTAS PARA IGNORAR NO CONTEXTO (Mas manter no lugar)
IGNORE_DIRS = {
    "node_modules", ".next", ".git", "__pycache__", "venv", ".venv", 
    "dist", "build", "Copy", ".temp_diff", ".expo", "test-results", 
    "playwright-report", "ignorar", "screenshots", "debug_screenshots",
    "output_sounds"
}

# 3. ARQUIVOS PARA IGNORAR NO CONTEXTO
IGNORE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "todososarquivos.txt", 
    "resposta.txt", ".DS_Store", "Thumbs.db", "icon.png", "splash.png",
    "adaptive-icon.png", "favicon.png", ".env" # .env ignorado por segurança e ruído
}

# 4. EXTENSÕES PROIBIDAS (Binários)
IGNORE_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".sqlite3", ".png", ".jpg", 
    ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot", 
    ".mp3", ".wav", ".mp4", ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", 
    ".exe", ".dll", ".bin"
}

# 5. ORDEM DE PRIORIDADE (Primacy Effect)
PRIORITY_ORDER = [
    "docs/Prompts/System_Instructions.xml",
    "docs/Prompts/Master_Handover_Executor.xml",
    "docs/MASTER_CONTEXT.md",
    "docs/ROADMAP.md",
    "docs/TASKS.md",
    "docs/TECH_DEBT.md",
    "docs/mobile/README.md",
    "app/models.py",
    "app/schemas.py",
    "mobile/src/store/auth.store.ts",
    "mobile/src/store/orders.store.ts"
]

def get_domain(filepath):
    """Detecta o domínio do arquivo baseado no caminho."""
    parts = filepath.replace("\\", "/").split("/")
    if "mobile" in parts: return "MOBILE"
    if "frontend" in parts: return "FRONTEND"
    if "app" in parts: return "BACKEND"
    if "docs" in parts: return "DOCUMENTATION"
    if "scripts" in parts: return "SHARED_INFRA"
    return "SHARED"

def move_trash_to_ignorar():
    """Move arquivos inúteis para a pasta ignorar/."""
    trash_path = Path(TRASH_FOLDER)
    if not trash_path.exists():
        trash_path.mkdir()
    
    moved_count = 0
    for pattern in TRASH_PATTERNS:
        p = Path(pattern)
        if p.exists():
            try:
                target = trash_path / p.name
                if p.is_dir():
                    if target.exists(): shutil.rmtree(target)
                    shutil.move(str(p), str(target))
                else:
                    shutil.move(str(p), str(target))
                print(f"🧹 Movido para {TRASH_FOLDER}: {pattern}")
                moved_count += 1
            except Exception as e:
                print(f"⚠️ Erro ao mover {pattern}: {e}")
    return moved_count

def generate_context():
    print(f"🚀 Iniciando Zeladoria MesaFlow...")
    
    # Passo 1: Limpeza física
    moved = move_trash_to_ignorar()
    
    # Passo 2: Mapeamento
    root = Path(".")
    all_files = []
    
    for p in root.rglob("*"):
        if p.is_file():
            rel_path = p.relative_to(root)
            path_str = str(rel_path).replace("\\", "/")
            
            # Filtros de exclusão
            if any(part in IGNORE_DIRS for part in rel_path.parts): continue
            if p.name in IGNORE_FILES: continue
            if p.suffix.lower() in IGNORE_EXTENSIONS: continue
            
            all_files.append(path_str)

    # Ordenação por prioridade (Refatorada para evitar ValueError)
    def sort_key(f):
        if f in PRIORITY_ORDER:
            return (0, PRIORITY_ORDER.index(f))
        return (1, f) # Peso 1 + ordem alfabética para o resto

    all_files.sort(key=sort_key)

    print(f"📄 Gerando {OUTPUT_FILE} ({len(all_files)} arquivos)...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # Header de Governança
        out.write(f"# MESAFLOW ARCHITECT CONTEXT\n")
        out.write(f"# GENERATED: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
        out.write(f"# TOTAL FILES: {len(all_files)}\n\n")

        for filepath in all_files:
            p = Path(filepath)
            try:
                size_kb = p.stat().st_size / 1024
                domain = get_domain(filepath)
                
                print(f"   Ingerindo [{domain}] {filepath} ({size_kb:.1f} KB)")
                
                out.write(f"# FILE: {filepath}\n")
                out.write(f"# DOMAIN: {domain}\n")
                out.write(f"# SIZE: {size_kb:.1f} KB\n")
                
                content = p.read_text(encoding="utf-8", errors="ignore")
                out.write("```\n")
                out.write(content)
                if not content.endswith("\n"): out.write("\n")
                out.write("```\n\n")
            except Exception as e:
                print(f"⚠️ Erro ao processar {filepath}: {e}")
                out.write(f"// Error reading file {filepath}: {e}\n\n")

    print(f"✨ Sucesso! Contexto gerado em {OUTPUT_FILE}")
    if moved > 0:
        print(f"💡 {moved} itens obsoletos foram movidos para a pasta '{TRASH_FOLDER}/'.")

if __name__ == "__main__":
    generate_context()
