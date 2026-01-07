import os
import shutil
import re
from pathlib import Path
import hashlib
from datetime import datetime, timezone

# ==============================================================================
# CONFIGURAÇÃO DE GOVERNANÇA DE CONTEXTO (v9.4 - Test Compatible)
# ==============================================================================

OUTPUT_FILE = "todososarquivos.txt"
TRASH_FOLDER = "ignorar"

IGNORE_DIRS = {
    "node_modules", ".next", ".git", "__pycache__", "venv", ".venv", 
    "dist", "build", "Copy", ".temp_diff", ".expo", "test-results", 
    "playwright-report", "ignorar", "screenshots", "debug_screenshots",
    "output_sounds"
}

IGNORE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "todososarquivos.txt", 
    "resposta.txt", ".DS_Store", "Thumbs.db", "icon.png", "splash.png",
    "adaptive-icon.png", "favicon.png", ".env"
}

IGNORE_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".sqlite3", ".png", ".jpg", 
    ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot", 
    ".mp3", ".wav", ".mp4", ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", 
    ".exe", ".dll", ".bin"
}

PRIORITY_ORDER = [
    "docs/Prompts/System_Instructions.xml",
    "docs/Prompts/Master_Handover_Executor.xml",
    "docs/MASTER_CONTEXT.md",
    "docs/ROADMAP.md",
    "docs/TASKS.md",
    "app/models.py",
    "app/schemas.py"
]

# --- FUNÇÕES UTILITÁRIAS (Expostas para Testes) ---

def is_ignored(path_str, patterns=None):
    """Verifica se um arquivo deve ser ignorado."""
    path = Path(path_str)
    if any(part in IGNORE_DIRS for part in path.parts): return True
    if path.name in IGNORE_FILES: return True
    if path.suffix.lower() in IGNORE_EXTENSIONS: return True
    return False

def is_test_file(path_str):
    """Detecta se o arquivo é de teste."""
    path = path_str.lower()
    return "test_" in path or "spec.ts" in path or "tests/" in path

def check_secrets(content, filename):
    """Detecta possíveis segredos no código."""
    patterns = [r"sk_live_[a-zA-Z0-9]+", r"APP_USR-[a-zA-Z0-9-]+"]
    warnings = []
    for p in patterns:
        if re.search(p, content):
            warnings.append(f"⚠️ POSSÍVEL SEGREDO DETECTADO em {filename}")
    return warnings

def minify_content(content):
    """Remove ruído excessivo do código."""
    return re.sub(r'\n\s*\n', '\n\n', content)

def get_dependencies():
    """Resumo de dependências do projeto."""
    return "FastAPI, SQLAlchemy, Next.js, React Native, Redis"

# --- CORE ---

def get_domain(filepath):
    parts = filepath.replace("\\", "/").split("/")
    if "mobile" in parts: return "MOBILE"
    if "frontend" in parts: return "FRONTEND"
    if "app" in parts: return "BACKEND"
    if "docs" in parts: return "DOCUMENTATION"
    if "scripts" in parts: return "SHARED_INFRA"
    return "SHARED"

def generate_context():
    print(f"🚀 Gerando Contexto MesaFlow...")
    root = Path(".")
    all_files = []
    for p in root.rglob("*"):
        if p.is_file():
            rel_path = str(p.relative_to(root)).replace("\\", "/")
            if not is_ignored(rel_path):
                all_files.append(rel_path)

    def sort_key(f):
        if f in PRIORITY_ORDER: return (0, PRIORITY_ORDER.index(f))
        return (1, f)
    all_files.sort(key=sort_key)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"# MESAFLOW ARCHITECT CONTEXT | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n")
        for filepath in all_files:
            p = Path(filepath)
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                out.write(f"# FILE: {filepath} | DOMAIN: {get_domain(filepath)}\n")
                out.write("```\n" + content + "\n```\n\n")
            except Exception as e:
                print(f"⚠️ Erro em {filepath}: {e}")

def main():
    generate_context()

if __name__ == "__main__":
    main()
