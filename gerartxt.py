import os

# ================================
# CONFIGURAÇÃO
# ================================

ARQUIVO_SAIDA = "todososarquivos.txt"

# Arquivos que devem aparecer no início do TXT (Ordem de leitura da IA)
PRIORIDADE_ARQUIVOS = [
    "communication.xml",
    "docs/ROADMAP.md",
    "readme.md",
    "app/models.py",
    "app/schemas.py",
    "app/main.py"
]

IGNORAR_PASTAS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", 
    ".idea", ".vscode", "dist", "build", ".next", "Copy"
}

IGNORAR_EXTENSOES = {
    ".pyc", ".exe", ".dll", ".so", ".zip", ".tar", ".gz", 
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".ico", 
    ".pdf", ".mp4", ".wav", ".mp3", ".svg", ".woff", ".woff2", ".ttf"
}

IGNORAR_ARQUIVOS_EXATOS = {
    ARQUIVO_SAIDA,
    "package-lock.json",
    "package.json",
    "tsconfig.json",
    "next.config.mjs",
    "postcss.config.mjs",
    "tailwind.config.ts",
    "eslint.config.mjs",
    "next-env.d.ts",
    ".gitignore",
    "pytest.ini"
}

BASE_DIR = os.path.normpath(os.getcwd())

# ================================
# FUNÇÕES
# ================================

def deve_ignorar(caminho_relativo: str) -> bool:
    partes = caminho_relativo.split(os.sep)
    
    # Ignorar pastas
    if any(p in IGNORAR_PASTAS for p in partes):
        return True

    nome_arquivo = os.path.basename(caminho_relativo)

    # Ignorar arquivos sensíveis ou exatos
    if nome_arquivo in IGNORAR_ARQUIVOS_EXATOS or nome_arquivo.startswith(".env"):
        return True

    # Ignorar extensões
    _, ext = os.path.splitext(nome_arquivo)
    return ext.lower() in IGNORAR_EXTENSOES

def coletar_arquivos():
    arquivos_prioridade = []
    arquivos_comuns = []

    for root, dirs, files in os.walk("."):
        # Modifica dirs in-place para não entrar em pastas ignoradas
        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]

        for file in files:
            caminho = os.path.join(root, file)
            caminho_relativo = os.path.relpath(caminho, ".")
            caminho_normalizado = caminho_relativo.replace("\\", "/")

            if deve_ignorar(caminho_relativo):
                continue

            if caminho_normalizado in PRIORIDADE_ARQUIVOS:
                arquivos_prioridade.append(caminho_relativo)
            else:
                arquivos_comuns.append(caminho_relativo)

    # Ordena os arquivos de prioridade conforme a lista definida
    arquivos_prioridade.sort(key=lambda x: PRIORIDADE_ARQUIVOS.index(x.replace("\\", "/")))
    # Ordena os comuns alfabeticamente
    arquivos_comuns.sort()

    return arquivos_prioridade + arquivos_comuns

def main():
    if os.path.exists(ARQUIVO_SAIDA):
        os.remove(ARQUIVO_SAIDA)

    lista_final = coletar_arquivos()
    
    print(f"🔍 Coletando {len(lista_final)} arquivos...")

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as saida:
        for caminho in lista_final:
            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    conteudo = f.read()
                
                ext = os.path.splitext(caminho)[1].replace(".", "")
                if not ext: ext = "txt"

                saida.write(f"\n# {caminho.replace('\\', '/')}\n")
                saida.write("```" + ext + "\n")
                saida.write(conteudo)
                if not conteudo.endswith("\n"):
                    saida.write("\n")
                saida.write("```\n")
                print(f" ✅ Incluído: {caminho}")
            except Exception as e:
                print(f" ❌ Erro ao ler {caminho}: {e}")

    print(f"\n🚀 Contexto gerado com sucesso em '{ARQUIVO_SAIDA}'")

if __name__ == "__main__":
    main()