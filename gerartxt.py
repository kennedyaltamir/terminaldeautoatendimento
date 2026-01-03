import os

# ================================
# CONFIGURAÇÃO
# ================================

ARQUIVO_SAIDA = "todososarquivos.txt"

IGNORAR_PASTAS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build"
}

IGNORAR_EXTENSOES = {
    ".pyc",
    ".exe",
    ".dll",
    ".so",
    ".zip",
    ".tar",
    ".gz",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".mp4",
    ".wav",
    ".mp3"
}

IGNORAR_ARQUIVOS_EXATOS = {
    ARQUIVO_SAIDA,
    ".env",
    ".env.local",
    ".env.dev",
    ".env.prod"
}

# 🔥 Caminhos absolutos a serem ignorados
BASE_DIR = os.path.normpath(os.getcwd())

IGNORAR_CAMINHOS_ABSOLUTOS = {
    os.path.normpath(os.path.join(BASE_DIR, "docs", "Prompts")),
    os.path.normpath(os.path.join(BASE_DIR, "frontend", ".next")),
}

# ================================
# FUNÇÕES
# ================================

def deve_ignorar(caminho_relativo: str) -> bool:
    caminho_absoluto = os.path.normpath(os.path.abspath(caminho_relativo))

    # Ignorar caminhos absolutos específicos
    for caminho_ignorado in IGNORAR_CAMINHOS_ABSOLUTOS:
        if caminho_absoluto.startswith(caminho_ignorado):
            return True

    partes = caminho_relativo.split(os.sep)

    # Ignorar pastas por nome
    for parte in partes:
        if parte in IGNORAR_PASTAS:
            return True

    nome_arquivo = os.path.basename(caminho_relativo)

    # Ignorar arquivos exatos
    if nome_arquivo in IGNORAR_ARQUIVOS_EXATOS:
        return True

    # Ignorar qualquer arquivo .env*
    if nome_arquivo.startswith(".env"):
        return True

    _, ext = os.path.splitext(nome_arquivo)
    return ext.lower() in IGNORAR_EXTENSOES


def main():
    # Remove versão anterior
    if os.path.exists(ARQUIVO_SAIDA):
        os.remove(ARQUIVO_SAIDA)

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as saida:
        for root, dirs, files in os.walk("."):
            root_abs = os.path.normpath(os.path.abspath(root))

            # Remove pastas ignoradas por nome
            dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]

            # Remove pastas ignoradas por caminho absoluto
            dirs[:] = [
                d for d in dirs
                if not any(
                    os.path.normpath(os.path.join(root_abs, d)).startswith(caminho)
                    for caminho in IGNORAR_CAMINHOS_ABSOLUTOS
                )
            ]

            for file in files:
                caminho = os.path.join(root, file)
                caminho_relativo = os.path.relpath(caminho, ".")

                if deve_ignorar(caminho_relativo):
                    continue

                try:
                    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                        conteudo = f.read()
                except Exception:
                    continue

                ext = os.path.splitext(file)[1].replace(".", "")

                saida.write("\n---\n\n")
                saida.write(f"## 📄 Arquivo: {caminho_relativo}\n\n")
                saida.write(f"```{ext}\n")
                saida.write(conteudo)
                if not conteudo.endswith("\n"):
                    saida.write("\n")
                saida.write("```\n")

        saida.write("\n---\n")

    print(f"✅ Contexto gerado com sucesso em '{ARQUIVO_SAIDA}'")


# ================================
# ENTRYPOINT
# ================================

if __name__ == "__main__":
    main()
