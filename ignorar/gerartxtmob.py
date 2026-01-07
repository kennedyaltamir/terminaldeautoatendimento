import os
import sys
import re
import argparse
import datetime
import fnmatch
import json
import subprocess
from pathlib import Path
from collections import defaultdict

# Tentativa de importar Rich para uma UI profissional
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    from rich.tree import Tree
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

# ============================================================
# CONFIGURAÇÃO (Mobile-Only Edition)
# ============================================================

ARQUIVO_SAIDA = "contexto_mobile.txt"
MAX_FILE_SIZE = 500 * 1024  # 500KB
TOKEN_LIMIT_WARNING = 150000 

# Ordem de importância para a IA (Primacy Effect)
PRIORITY_ORDER = [
    "docs/mobile/README.md",
    "docs/mobile/architecture/MOBILE_ARCHITECTURE.md",
    "docs/mobile/architecture/APP_ARCHITECTURE.md",
    "mobile/app.json",
    "mobile/package.json",
    "mobile/tsconfig.json",
    "mobile/App.tsx",
    "scripts/setup/verify_mobile_setup.py"
]

# Pastas a serem incluídas (Filtro de Inclusão)
INCLUDE_PATHS = ["mobile", "docs/mobile"]

IGNORAR_PASTAS = {
    ".git", "node_modules", ".next", "__pycache__", 
    "venv", ".venv", ".pytest_cache", "Copy", 
    ".temp_diff", ".update_transaction", "dist", "build", 
    ".vscode", ".idea", "coverage", "playwright-report", "test-results",
    "assets", "public", "output_sounds", "screenshots", ".expo"
}

IGNORAR_EXTENSOES = {
    ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".sqlite3", 
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", 
    ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".wav", 
    ".mp4", ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", 
    ".exe", ".dll", ".so", ".log", ".bak", ".tag", ".lock"
}

IGNORAR_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", 
    "todososarquivos.txt", "contexto_mobile.txt", "resposta.txt", ".DS_Store", "Thumbs.db",
    "atualizar.log", "test.db", "ngrok.exe"
}

SECRET_PATTERNS = {
    "Stripe Key": r"(sk_live_[0-9a-zA-Z]{24})",
    "MercadoPago Token": r"(APP_USR-[0-9]{16}-[0-9]{6}-[a-z0-9]{32}-[0-9]{9})",
    "Generic Secret": r"(?i)(api_?key|secret|password|token)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{20,})['\"]"
}

# ============================================================
# MOTOR DE INTELIGÊNCIA
# ============================================================

class ProjectIntelligence:
    def __init__(self):
        self.imports = defaultdict(list)
        self.component_props = {}

    def analyze(self, filepath, content):
        ext = os.path.splitext(filepath)[1]
        
        # Análise de Dependências (JS/TS/TSX)
        if ext in [".ts", ".tsx", ".js", ".jsx"]:
            matches = re.findall(r"import\s+.*\s+from\s+['\"](.*)['\"]", content)
            for m in matches:
                self.imports[filepath].append(m)

            # Extração de Props (React Native)
            if "interface" in content and "Props" in content:
                props_match = re.findall(r"interface\s+(\w+Props)\s*{([^}]+)}", content, re.DOTALL)
                for name, body in props_match:
                    clean_body = re.sub(r"\s+", " ", body).strip()
                    self.component_props[filepath] = f"{name}: {{ {clean_body} }}"

    def get_dependency_graph(self):
        graph = ["## MOBILE DEPENDENCY GRAPH"]
        for file, deps in self.imports.items():
            if deps:
                clean_deps = [d for d in deps if not d.startswith(".")]
                if clean_deps:
                    graph.append(f"- {os.path.basename(file)} -> {', '.join(clean_deps[:3])}...")
        return "\n".join(graph)

def redact_secrets(content):
    redacted_count = 0
    for name, pattern in SECRET_PATTERNS.items():
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, f"[REDACTED_{name.upper()}]", content)
            redacted_count += len(matches)
    return content, redacted_count

def get_priority_score(filepath):
    filepath = filepath.replace("\\", "/")
    for i, priority_path in enumerate(PRIORITY_ORDER):
        if priority_path in filepath:
            return i
    return 999

def generate_tree(startpath):
    tree = []
    for root, dirs, files in os.walk(startpath):
        rel_root = os.path.relpath(root, startpath).replace("\\", "/")
        
        # Só mostra na árvore o que for mobile ou docs/mobile
        if rel_root != "." and not any(rel_root.startswith(p) for p in INCLUDE_PATHS):
            continue

        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        tree.append(f"{indent}├── {os.path.basename(root)}/")
        subindent = '│   ' * (level + 1)
        for f in files:
            if f in IGNORAR_FILES: continue
            if not any(f.endswith(ext) for ext in IGNORAR_EXTENSOES):
                tree.append(f"{subindent}├── {f}")
    return "\n".join(tree)

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="MesaFlow Mobile Context Generator")
    parser.add_argument("--no-minify", action="store_true", help="Mantém espaços em branco")
    args = parser.parse_args()

    if HAS_RICH:
        console.print(Panel.fit("📱 [bold orange1]MesaFlow Mobile[/bold orange1] | Context Generator", border_style="orange1"))
    else:
        print("--- MesaFlow Mobile Context Generator ---")

    intel = ProjectIntelligence()
    all_files = []
    
    for root, dirs, files in os.walk("."):
        rel_root = os.path.relpath(root, ".").replace("\\", "/")
        
        # Filtro de Inclusão Estrito
        if not any(rel_root.startswith(p) for p in INCLUDE_PATHS) and "mobile" not in rel_root.lower():
            continue

        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
        
        for file in files:
            if any(file.endswith(ext) for ext in IGNORAR_EXTENSOES): continue
            if file in IGNORAR_FILES: continue
            
            filepath = os.path.join(root, file)
            if os.path.getsize(filepath) > MAX_FILE_SIZE: continue
            all_files.append(filepath)

    # Ordenação por Prioridade
    all_files.sort(key=lambda x: (get_priority_score(x), x))

    output = []
    output.append(f"# MESAFLOW MOBILE CONTEXT - GENERATED {datetime.datetime.now()}\n")
    output.append("## MOBILE STRUCTURE\n```text\n" + generate_tree(".") + "\n```\n")
    
    stats = {"files": 0, "chars": 0, "redacted": 0}

    def process():
        nonlocal stats
        for filepath in all_files:
            rel_path = os.path.relpath(filepath, ".").replace("\\", "/")
            
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                intel.analyze(rel_path, content)
                content, redacted = redact_secrets(content)
                stats["redacted"] += redacted

                if not args.no_minify:
                    content = re.sub(r'\n\s*\n', '\n\n', content)

                header = f"\n# FILE: {rel_path}\n"
                formatted = f"{header}```\n{content}\n```\n"
                
                output.append(formatted)
                stats["files"] += 1
                stats["chars"] += len(formatted)
                
                if not HAS_RICH: print(f"📄 [OK] {rel_path}")

            except Exception as e:
                print(f"❌ [ERRO] {rel_path}: {e}")

    if HAS_RICH:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Processando arquivos mobile...", total=len(all_files))
            process()
    else:
        process()

    output.append("\n" + intel.get_dependency_graph() + "\n")
    
    if intel.component_props:
        output.append("## MOBILE COMPONENT PROPS\n")
        for comp, props in intel.component_props.items():
            output.append(f"- **{comp}**: {props}\n")

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write("".join(output))

    tokens_est = int(stats["chars"] / 4)
    
    if HAS_RICH:
        table = Table(title="Resumo do Contexto Mobile")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta")
        table.add_row("Arquivos Mobile", str(stats["files"]))
        table.add_row("Segredos Redigidos", str(stats["redacted"]))
        table.add_row("Tokens Estimados", f"{tokens_est:,}")
        console.print(table)
        console.print(f"\n✅ [bold green]Arquivo '{ARQUIVO_SAIDA}' gerado![/bold green]")
    else:
        print(f"\n✅ Gerado: {ARQUIVO_SAIDA} ({stats['files']} arquivos, ~{tokens_est} tokens)")

if __name__ == "__main__":
    main()
