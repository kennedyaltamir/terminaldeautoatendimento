# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:55:00
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

OUTPUT_FILE = "todososarquivos.txt"

# ====================================================================================================
# 1. LISTA DE PRIORIDADE ABSOLUTA (TOP 9)
# ====================================================================================================
PRIORITY_ORDER = [
    "docs/governance/AI_STARTUP_SEQUENCE.xml",
    "docs/governance/CONTEXT_PRIORITY_PROTOCOL.md",
    "docs/Prompts/System_Persona.xml",
    "docs/governance/AI_ROLE_PROTOCOL.md",
    "docs/governance/FAIL_FAST_PROTOCOL.md",
    "docs/governance/UPDATE_EXECUTION_PROTOCOL.md",
    "docs/governance/ERROR_RESPONSE_MAPPING_PROTOCOL.md",
    "docs/TASKS.md",
    "docs/ROADMAP.md"
]

# ====================================================================================================
# 2. FILTROS DE RUÍDO (BLOCKLIST)
# ====================================================================================================
IGNORE_PATTERNS = {
    ".git", ".vscode", ".idea", ".ds_store",
    "node_modules", "venv", ".venv", "__pycache__", ".pytest_cache",
    ".next", "dist", "build", "coverage", "test-results", "playwright-report",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock",
    "todososarquivos.txt", "documentacao_completa.txt", "resposta.txt",
    "atualizar.log", "copy", ".temp_diff", "ignorar",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp",
    ".mp3", ".wav", ".mp4", ".mov", ".jar",
    ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", ".exe", ".dll", ".so",
    ".apk", ".aab", ".keystore", ".jks", ".ttf", ".otf", ".woff", ".woff2",
    "cpp.o", ".dir", ".mako", ".template", ".keep", ".ps1", ".sh"
}

IGNORE_PATHS = {
    "mobile/android/app/build",
    "mobile/android/.gradle",
    "mobile/ios",
    "frontend/.next",
    "ignorar"
}

SENSITIVE_FILES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "env.prod", "frontend.env.local", "credentials.json",
    "service_account.json", "google-services.json", ".env.example"
}

def get_file_metadata(path_obj: Path) -> str:
    try:
        mtime = path_obj.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "UNKNOWN"

def is_ignored(path_obj: Path) -> bool:
    rel_path = str(path_obj).replace("\\", "/")
    for ignore_path in IGNORE_PATHS:
        if rel_path.startswith(ignore_path):
            return True
    if path_obj.name in SENSITIVE_FILES:
        return True
    if path_obj.name.lower() in IGNORE_PATTERNS:
        return True
    if path_obj.suffix.lower() in IGNORE_PATTERNS:
        return True
    for part in path_obj.parts:
        if part.lower() in IGNORE_PATTERNS:
            return True
    return False

def get_domain(filepath: str) -> str:
    parts = filepath.split("/")
    if "mobile" in parts: return "MOBILE"
    if "frontend" in parts: return "FRONTEND"
    if "app" in parts: return "BACKEND"
    if "docs" in parts: return "DOCUMENTATION"
    if "scripts" in parts: return "DEVOPS_SCRIPTS"
    return "ROOT_CONFIG"

def estimate_tokens(text: str) -> int:
    # Heurística simples: 1 token ~= 4 caracteres
    return len(text) // 4

def generate_context():
    print("Gerador de Contexto v2.4 (Mobile Enabled)")
    print(f"{'ARQUIVO':<60} | {'TOKENS':>10} | {'STATUS':<10}")
    print("-" * 85)
    root = Path(".")
    files_to_process = []
    total_tokens = 0
    for p in root.rglob("*"):
        if p.is_file() and not is_ignored(p):
            files_to_process.append(p)

    def sort_key(p):
        path_str = str(p).replace("\\", "/")
        if path_str in PRIORITY_ORDER:
            return (0, PRIORITY_ORDER.index(path_str))
        if path_str.startswith("mobile/"): return (1, path_str)
        if path_str.startswith("frontend/"): return (2, path_str)
        if path_str.startswith("app/"): return (3, path_str)
        return (4, path_str)

    files_to_process.sort(key=sort_key)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"<!-- MESAFLOW CONTEXT BUNDLE -->\n")
        out.write(f"<!-- GENERATED_AT: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC -->\n")
        for p in files_to_process:
            rel = str(p).replace("\\", "/")
            mod = get_file_metadata(p)
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                content = re.sub(r'\n\s*\n', '\n', content) # Remove linhas vazias consecutivas
                tokens = estimate_tokens(content)
                total_tokens += tokens
                tag_start = "[[" + "MESAFLOW_BEGIN:"
                tag_end = "[[" + "MESAFLOW_END]]"
                # Cabeçalho Otimizado
                out.write(f"{tag_start}{rel}]]\n")
                out.write(f"# DOMAIN: {get_domain(rel)}\n")
                out.write(f"# LAST_MODIFIED: {mod}\n")
                out.write(content)
                if not content.endswith("\n"):
                    out.write("\n")
                out.write(f"{tag_end}\n") # Apenas uma quebra de linha entre arquivos
                print(f"[OK] {rel:<60} | {tokens:>10}")
            except Exception as e:
                print(f"[ERRO] {rel:<60} | {str(e)}")
    print("-" * 85)
    print(f"Contexto gerado em: {OUTPUT_FILE}")
    print(f"Total Estimado de Tokens: {total_tokens}")

if __name__ == "__main__":
    generate_context()
