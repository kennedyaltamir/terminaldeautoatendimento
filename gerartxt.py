import os
import sys
import re
import argparse
import datetime
import fnmatch
import json
from pathlib import Path

# Tenta importar pyperclip para clipboard, falha graciosamente se não existir
try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

# ============================================================
# CONFIGURAÇÃO (V3.4 - Aggressive Filtering)
# ============================================================

ARQUIVO_SAIDA = "todososarquivos.txt"
MAX_FILE_SIZE = 500 * 1024  # 500KB

# Pastas para ignorar completamente
IGNORAR_PASTAS = {
    ".git", "node_modules", ".next", "__pycache__", 
    "venv", ".venv", ".pytest_cache", "Copy", 
    ".temp_diff", ".update_transaction", "dist", "build", 
    ".vscode", ".idea", "coverage", "playwright-report", "test-results",
    "assets", "public",
    "docs/tasks", "docs/testes" # Ignora tarefas antigas e lixo de teste
}

# Extensões binárias
IGNORAR_EXTENSOES = {
    ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".sqlite3", 
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", 
    ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".wav", 
    ".mp4", ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", 
    ".exe", ".dll", ".so", ".log", ".bak", ".tag", ".lock"
}

IGNORAR_ARQUIVOS_EXATOS = {
    ARQUIVO_SAIDA, "resposta.txt", "package-lock.json", "yarn.lock", 
    "pnpm-lock.yaml", "atualizar.log", "dummy.txt"
}

# Regex para detecção básica de segredos
SECRET_PATTERNS = [
    r"(?i)(api_?key|secret|password|token)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]",
    r"sk_live_[0-9a-zA-Z]{24}",
]

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def load_gitignore():
    """Lê o .gitignore e retorna uma lista de padrões."""
    patterns = []
    if os.path.exists(".gitignore"):
        try:
            with open(".gitignore", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        except Exception:
            pass
    return patterns

def is_ignored(path, gitignore_patterns):
    """Verifica se o caminho deve ser ignorado."""
    # Normalização Crítica para Windows
    path = path.replace("/", os.sep).replace("\\", os.sep)
    
    name = os.path.basename(path)
    parts = path.split(os.sep)
    
    # 1. Pastas Proibidas
    # Verifica se qualquer parte do caminho está na lista negra
    # Normaliza as pastas ignoradas para o separador do sistema
    normalized_ignores = {p.replace("/", os.sep) for p in IGNORAR_PASTAS}
    
    # Verifica correspondência exata de pasta ou subpasta
    for part in parts:
        if part in normalized_ignores:
            return True
            
    # Verifica caminhos compostos (ex: docs/tasks)
    for ignore in normalized_ignores:
        if ignore in path:
            return True
    
    # 2. Arquivos Exatos
    if name in IGNORAR_ARQUIVOS_EXATOS: return True
    
    # 3. Extensões
    _, ext = os.path.splitext(name)
    if ext.lower() in IGNORAR_EXTENSOES: return True
    
    # 4. Gitignore
    for pattern in gitignore_patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(path, pattern):
            return True
            
    return False

def check_secrets(content, filepath):
    """Verifica se há segredos hardcoded no conteúdo."""
    warnings = []
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content):
            warnings.append(f"⚠️  POSSÍVEL SEGREDO em {filepath}")
    return warnings

def minify_content(content):
    """Remove linhas em branco consecutivas."""
    return re.sub(r'\n\s*\n', '\n\n', content)

def get_dependencies():
    """Extrai resumo de dependências para o topo do arquivo."""
    deps = []
    # Python
    if os.path.exists("requirements.txt"):
        deps.append("\n# --- requirements.txt (Summary) ---")
        try:
            with open("requirements.txt", "r", encoding="utf-8") as f:
                deps.append(f.read())
        except: pass
    
    # Node
    if os.path.exists("frontend/package.json"):
        try:
            with open("frontend/package.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                deps.append("\n# --- package.json (Dependencies) ---")
                deps.append(json.dumps(data.get("dependencies", {}), indent=2))
        except: pass
        
    return "\n".join(deps) + "\n"

def generate_tree(startpath, gitignore_patterns, focus=None):
    """Gera uma string de árvore de diretórios."""
    tree_str = "📂 Estrutura do Projeto:\n.\n"
    
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), gitignore_patterns)]
        
        # Lógica de foco na árvore
        rel_root = os.path.relpath(root, startpath)
        if focus and rel_root != "." and not rel_root.startswith(focus) and not focus.startswith(rel_root):
            continue

        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level)
        subindent = '│   ' * (level + 1)
        
        if root != startpath:
            tree_str += f"{indent}├── {os.path.basename(root)}/\n"
            
        for f in files:
            if not is_ignored(os.path.join(root, f), gitignore_patterns):
                tree_str += f"{subindent}├── {f}\n"
                
    return tree_str

def is_test_file(path):
    """Detecta arquivos de teste."""
    path = path.replace("/", os.sep).replace("\\", os.sep)
    parts = path.split(os.sep)
    
    # Se estiver em qualquer pasta de teste
    if "tests" in parts or "functional" in parts or "e2e" in parts:
        return True
        
    return os.path.basename(path).startswith("test_") or path.endswith(".spec.ts")

# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Gerador de Contexto Otimizado v3.4")
    parser.add_argument("--focus", help="Focar apenas em uma pasta específica")
    parser.add_argument("--no-minify", action="store_true", help="Desativar minificação")
    parser.add_argument("--copy", action="store_true", help="Copiar para o clipboard")
    args = parser.parse_args()

    print(f"🔍 Iniciando Gerador de Contexto v3.4...")
    
    gitignore = load_gitignore()
    output_buffer = []
    
    # 1. Tree
    print("🌳 Gerando mapa visual...")
    output_buffer.append(generate_tree(".", gitignore, args.focus))
    
    # 2. Dependencies
    print("📦 Coletando dependências...")
    output_buffer.append(get_dependencies())
    
    output_buffer.append("\n" + "="*50 + "\nCONTEÚDO DOS ARQUIVOS\n" + "="*50 + "\n")

    total_chars = 0
    file_count = 0
    warnings = []

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), gitignore)]
        
        if args.focus:
             rel = os.path.relpath(root, ".")
             if rel != "." and not rel.startswith(args.focus) and not args.focus.startswith(rel):
                 continue

        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, ".").replace("\\", "/")
            
            if is_ignored(filepath, gitignore): continue
            if args.focus and not rel_path.startswith(args.focus): continue

            try:
                size = os.path.getsize(filepath)
                if size > MAX_FILE_SIZE:
                    print(f"⚠️  Ignorado (Muito grande): {rel_path}")
                    continue
            except: continue

            file_count += 1
            print(f"📄 [INCLUÍDO] {rel_path}")

            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
            header = f"\n# FILE: {rel_path}\n# SIZE: {size} bytes | MODIFIED: {mtime}\n"
            
            try:
                if is_test_file(filepath):
                    content = "# [TEST CONTENT EXCLUDED] Refer to codebase for full test implementation.\n"
                else:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    file_warnings = check_secrets(content, rel_path)
                    warnings.extend(file_warnings)

                    if not args.no_minify:
                        content = minify_content(content)

                ext = os.path.splitext(file)[1].replace(".", "") or "txt"
                formatted = f"{header}```{ext}\n{content}\n```\n"
                
                output_buffer.append(formatted)
                total_chars += len(formatted)

            except Exception as e:
                print(f"❌ Erro ao ler {rel_path}: {e}")

    full_content = "".join(output_buffer)
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write(full_content)

    print("\n" + "="*50)
    print(f"✅ Contexto gerado em: {ARQUIVO_SAIDA}")
    print(f"📦 Arquivos processados: {file_count}")
    print(f"🧠 Estimativa de Tokens: ~{int(total_chars / 4)}")
    
    if warnings:
        print("\n🚨 ALERTAS DE SEGURANÇA:")
        for w in warnings: print(w)
    
    if args.copy and HAS_CLIPBOARD:
        try:
            pyperclip.copy(full_content)
            print("\n📋 Copiado para o clipboard!")
        except: pass

if __name__ == "__main__":
    main()