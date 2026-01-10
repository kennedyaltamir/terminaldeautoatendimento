import os

# Configuração
OUTPUT_FILE = "todososarquivos.txt"

# Pastas para ignorar completamente
IGNORE_DIRS = {
    "node_modules", ".next", ".git", "__pycache__", "venv", ".venv", 
    "dist", "build", "coverage", ".pytest_cache", "Copy", ".vscode", ".idea"
}

# Extensões para ignorar (binários, imagens, etc)
IGNORE_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".sqlite3", 
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot", 
    ".mp3", ".wav", ".mp4", ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", ".exe", ".dll"
}

# Arquivos específicos para ignorar
IGNORE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", 
    "todososarquivos.txt", "resposta.txt", ".DS_Store", "Thumbs.db"
}

# Ordem de prioridade no arquivo final (para a IA ler primeiro o contexto)
PRIORITY_FILES = [
    "docs/Prompts/System_Instructions.xml",
    "docs/Prompts/Handover_Prompt.xml",
    "docs/ROADMAP.md",
    "docs/TASKS.md",
    "docs/MANUAL_GESTOR.md",
    "docs/MANUAL_COZINHA.md",
    "docs/MANUAL_GARCOM.md",
    "docs/MANUAL_DELIVERY.md",
    "docs/MANUAL_FINANCEIRO.md",
    "app/models.py",
    "app/schemas.py",
    "app/main.py",
    "frontend/src/types/index.ts"
]

def is_ignored(path):
    parts = path.split(os.sep)
    # Verifica pastas ignoradas
    for part in parts:
        if part in IGNORE_DIRS:
            return True
    
    filename = os.path.basename(path)
    # Verifica arquivos ignorados
    if filename in IGNORE_FILES:
        return True
    
    # Verifica extensões ignoradas
    _, ext = os.path.splitext(filename)
    if ext.lower() in IGNORE_EXTENSIONS:
        return True
        
    return False

def get_all_files(root_dir):
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        # Modifica dirs in-place para pular pastas ignoradas
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            file_path = os.path.join(root, file)
            if not is_ignored(file_path):
                file_list.append(file_path)
    return file_list

def generate_context():
    print(f"🔍 Mapeando arquivos em '{os.getcwd()}'...")
    all_files = get_all_files(".")
    
    # Normaliza caminhos para comparação (Windows/Linux)
    all_files = [f.replace("\\", "/") for f in all_files]
    
    # Separa prioritários e comuns
    priority_set = set(PRIORITY_FILES)
    found_priority = [f for f in all_files if f in priority_set]
    others = [f for f in all_files if f not in priority_set]
    
    # Ordena prioritários conforme a lista definida
    found_priority.sort(key=lambda x: PRIORITY_FILES.index(x))
    others.sort()
    
    final_list = found_priority + others
    
    print(f"📄 Gerando {OUTPUT_FILE} com {len(final_list)} arquivos...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for filepath in final_list:
            try:
                # Tenta ler o arquivo
                with open(filepath, "r", encoding="utf-8", errors="ignore") as infile:
                    content = infile.read()
                    
                    # Escreve o cabeçalho e o conteúdo
                    outfile.write(f"\n# {filepath}\n")
                    
                    # Detecta linguagem para markdown
                    ext = os.path.splitext(filepath)[1].lower()
                    lang = "text"
                    if ext in [".py"]: lang = "python"
                    elif ext in [".ts", ".tsx"]: lang = "typescript"
                    elif ext in [".js", ".jsx"]: lang = "javascript"
                    elif ext in [".html"]: lang = "html"
                    elif ext in [".css"]: lang = "css"
                    elif ext in [".json"]: lang = "json"
                    elif ext in [".md"]: lang = "markdown"
                    elif ext in [".xml"]: lang = "xml"
                    elif ext in [".sql"]: lang = "sql"
                    
                    outfile.write(f"```{lang}\n")
                    outfile.write(content)
                    # Garante quebra de linha no final
                    if not content.endswith("\n"):
                        outfile.write("\n")
                    outfile.write("```\n")
                    
            except Exception as e:
                print(f"⚠️ Erro ao ler {filepath}: {e}")

    print(f"✅ Sucesso! Arquivo '{OUTPUT_FILE}' gerado.")
    print("👉 Agora você pode enviar este arquivo junto com o prompt para a nova IA.")

if __name__ == "__main__":
    generate_context()