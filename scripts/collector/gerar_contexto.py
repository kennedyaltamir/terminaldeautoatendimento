import os
import hashlib
from datetime import datetime

OUTPUT_FILE = "todos_os_arquivos.txt"

# Diretórios ignorados
IGNORED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "backups"
}

# Extensões ignoradas
IGNORED_EXT = {
    ".pyc",
    ".zip",
    ".exe",
    ".dll",
    ".so"
}

def sha256_of_file(path: str) -> str:
    """Retorna o SHA-256 de um arquivo."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def collect_files(root: str):
    """Percorre todo o projeto retornando arquivos válidos."""
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORED_EXT:
                continue

            full_path = os.path.join(dirpath, file)
            rel_path = os.path.relpath(full_path, root)

            yield rel_path, full_path

def main():
    print("📦 GERADOR DE CONTEXTO — HyperOptimus Collector v1.0")
    print("   Iniciando coleta dos arquivos...\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # Cabeçalho Meta
        out.write("<!-- HYPEROPTIMUS CONTEXT BUNDLE -->\n")
        out.write(f"<!-- TIMESTAMP: {datetime.utcnow().isoformat()}Z -->\n")
        out.write("<!-- SYSTEM_MODE: HYPEROPTIMUS_ACTIVE -->\n")
        out.write("\n")

        for rel_path, full_path in collect_files("."):
            sha = sha256_of_file(full_path)

            out.write(f"[[MESAFLOW_BEGIN:{rel_path}]]\n")
            out.write(f"# FILE: {rel_path}\n")
            out.write(f"# SHA256: {sha}\n")
            out.write("# ------------------------------------------------------------\n")

            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"\n[ERRO AO LER ARQUIVO: {e}]\n")

            out.write("\n[[MESAFLOW_END]]\n\n")

    print("✅ CONTEXTO GERADO COM SUCESSO!")
    print(f"   Arquivo final: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
