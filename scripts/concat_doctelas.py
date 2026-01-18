# scripts/documentation/concat_doctelas.py
import os
from pathlib import Path

# Pasta raiz dos documentos
DOCS_ROOT = Path("doctelas")
OUTPUT_FILE = Path("docs/sds/ALL_DOCTELAS_CONCAT.md")

separator = "\n\n" + "#" * 80 + "\n\n"

def concat_docs():
    all_content = []

    for platform in ["web", "mobile"]:
        platform_path = DOCS_ROOT / platform
        if not platform_path.exists():
            continue

        for md_file in sorted(platform_path.glob("*.md")):
            try:
                content = md_file.read_text(encoding="utf-8")
                header = f"# Plataforma: {platform.upper()} | Arquivo: {md_file.name}\n"
                all_content.append(header + content + separator)
            except Exception as e:
                print(f"Erro ao ler {md_file}: {e}")

    # Salvar arquivo concatenado
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_content))

    print(f"✅ Todos os arquivos concatenados em: {OUTPUT_FILE}")

if __name__ == "__main__":
    concat_docs()
