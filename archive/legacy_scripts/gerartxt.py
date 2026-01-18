import os
import re
import json
import hashlib
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone

# ==============================================================================
# 🧬 MESAFLOW COGNITIVE HYPERBOOT v13.0
# ==============================================================================
# Autor: Optimus Architect
# Protocolos: RFC-001, RFC-003, RFC-007 (Soberania de Contexto)
# Novidades: Git Delta, Stub Filtering, Rigorous Binary Block, Whitespace Pruning.
# ==============================================================================

OUTPUT_FILE = "todososarquivos.txt"
KERNEL_LOG = "kernel_journal.jsonl"
CACHE_DIR = Path(".mesaflow_cache")

# RFC-003: Ordem de Ingestão Soberana (Governança v4.2)
KERNEL_FILES = [
    "MASTER_PROJECT_SPECIFICATION.md",
    "governance/registry.xml",
    "governance/prompts/AI_STARTUP_SEQUENCE.xml",
    "governance/prompts/AI_COGNITIVE_PROFILE.xml",
    "requirements.txt",
    "package.json",
]

# RFC-007: Bloqueio Rigoroso de Ruído e Binários
IGNORE_EXTENSIONS = {
    # Binários e Mídia
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".pdf",
    ".mp3", ".wav", ".mp4", ".webm", ".mov", ".jar", ".zip", ".tar", 
    ".gz", ".rar", ".7z", ".exe", ".dll", ".so", ".apk", ".aab",
    # Compilados e Caches
    ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".map", ".node"
}

IGNORE_PATTERNS = {
    ".git", ".vscode", ".idea", ".ds_store",
    "node_modules", "venv", ".venv", "__pycache__", ".pytest_cache",
    ".next", "dist", "build", "coverage", "test-results", "playwright-report",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock",
    "todososarquivos.txt", "documentacao_completa.txt", "resposta.txt",
    "atualizar.log", "copy", ".temp_diff", "ignorar", "backups",
    "kernel_journal.jsonl", "structure_audit.txt", "estrutura_atual.txt",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".mp4", ".webm",
        ".mp3", ".wav", ".mp4", ".mov", ".jar", ".probe",

    ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", ".exe", ".dll", ".so",
    ".apk", ".aab", ".keystore", ".jks", ".ttf", ".otf", ".woff", ".woff2",
    "cpp.o", ".dir", ".mako", ".template", ".keep", ".ps1", ".sh",
    ".bak", ".tmp", ".log", ".patch", ".class", ".java",".bin", ".lock"
}

IGNORE_PATHS = [
    "mobile/android/app/build",
    "mobile/android/.gradle",
    "mobile/ios",
    "frontend/.next",
    "ignorar",
    "backups",
    "testesvisuais",
    ".mesaflow_cache"
]

SENSITIVE_FILES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "credentials.json", "service_account.json", "google-services.json"
}

STUB_INDICATORS = [
    r"recovered as stub",
    r"STUB RECOVERED",
    r"placeholder",
    r"print\(['\"]Script.*recovered as stub\.['\"]\)"
]

def get_changed_files():
    """Implementa o modo Git Delta: detecta arquivos modificados ou novos."""
    try:
        # m: modificados, o: outros (novos/untracked), --exclude-standard: respeita .gitignore
        cmd = "git ls-files -m -o --exclude-standard"
        result = subprocess.check_output(cmd, shell=True).decode().splitlines()
        return [Path(f) for f in result if os.path.exists(f)]
    except Exception as e:
        print(f"⚠️ Erro ao consultar Git: {e}. Fallback para varredura total.")
        return None

def is_stub(content):
    """Filtra arquivos que não contêm lógica útil (apenas stubs de manutenção)."""
    for pattern in STUB_INDICATORS:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False

def is_ignored(path_obj):
    """Filtro rigoroso conforme RFC-007."""
    name = path_obj.name.lower()
    if name in SENSITIVE_FILES: return True
    if path_obj.suffix.lower() in IGNORE_EXTENSIONS: return True
    
    # Verifica se o caminho contém algum padrão de ignorar
    rel_path = str(path_obj).replace("\\", "/")
    if any(pattern in rel_path for pattern in IGNORE_PATTERNS):
        return True
    
    # Ignora arquivos ocultos (exceto os essenciais do projeto)
    if name.startswith(".") and name not in [".gitignore", ".env.example"]:
        return True
        
    return False

def get_domain(filepath):
    if "governance" in filepath: return "GOVERNANCE"
    if "mobile" in filepath: return "MOBILE"
    if "frontend" in filepath: return "FRONTEND"
    if "app" in filepath: return "BACKEND"
    if "scripts" in filepath: return "DEVOPS_SCRIPTS"
    return "ROOT_CONFIG"

def clean_content(content):
    """Remove ruído visual e compacta tokens."""
    # Remove triplas ou duplas linhas em branco
    content = re.sub(r'\n\s*\n', '\n', content)
    return content.strip()

def self_test():
    """Validação pré-boot (RFC-003)."""
    missing = [f for f in KERNEL_FILES if not Path(f).exists()]
    if missing:
        print(f"❌ Falha no Self-Test. Faltam Kernel Files: {missing}")
        return False
    return True

def generate_bootloader():
    parser = argparse.ArgumentParser(description="MesaFlow Context Generator")
    parser.add_argument("--changed", action="store_true", help="Modo Git Delta (Somente alterados)")
    parser.add_argument("--silent", action="store_true", help="Oculta logs detalhados")
    args = parser.parse_args()

    if not self_test(): return

    mode = "changed" if args.changed else "full"
    print(f"🚀 Iniciando Cognitive HyperBoot v13.0 [MODO: {mode.upper()}]")
    
    root = Path(".")
    files_to_process = []
    
    # 1. Seleção de Arquivos (Delta vs Full)
    if args.changed:
        changed = get_changed_files()
        if changed:
            # Kernel Files sempre são incluídos para dar contexto de lei à IA
            files_to_process = [Path(f) for f in KERNEL_FILES]
            for f in changed:
                if f not in files_to_process and not is_ignored(f):
                    files_to_process.append(f)
        else:
            print("✨ Nenhum arquivo alterado detectado. Nada a fazer.")
            return
    else:
        # Coleta total
        for p in root.rglob("*"):
            if p.is_file() and not is_ignored(p):
                files_to_process.append(p)

    # 2. Ordenação por Soberania (Kernel sempre no topo)
    files_to_process.sort(key=lambda x: (str(x) not in KERNEL_FILES, get_domain(str(x)), str(x)))

    total_tokens = 0
    processed_count = 0
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"<!-- MESAFLOW SYSTEM CONTEXT v13.0 | MODE: {mode} -->\n")
        out.write(f"<!-- TIMESTAMP: {datetime.now(timezone.utc).isoformat()} -->\n\n")

        for p in files_to_process:
            rel_path = str(p).replace("\\", "/")
            try:
                content_raw = p.read_text(encoding="utf-8", errors="ignore")
                
                if is_stub(content_raw): continue
                
                content = clean_content(content_raw)
                domain = get_domain(rel_path)
                mod_date = datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                out.write(f"[[MESAFLOW_BEGIN:{rel_path}]]\n")
                out.write(f"# DOMAIN: {domain}\n")
                out.write(f"# LAST_MODIFIED: {mod_date}\n")
                out.write(content + "\n")
                out.write(f"[[MESAFLOW_END]]\n\n")
                
                total_tokens += len(content) // 4 # Heurística de tokens
                processed_count += 1
                if not args.silent: print(f"   ✅ {domain}: {rel_path}")
                
            except Exception as e:
                print(f"   ❌ Erro em {rel_path}: {e}")

        # Summary para a IA receptora
        out.write(f"\n<Context_Summary>\n    files=\"{processed_count}\"\n    est_tokens=\"{total_tokens}\"\n    mode=\"{mode}\"\n</Context_Summary>\n")

    print("-" * 60)
    print(f"💾 Contexto gerado em: {OUTPUT_FILE}")
    print(f"📊 Arquivos: {processed_count} | Est. Tokens: ~{total_tokens}")

if __name__ == "__main__":
    generate_bootloader()