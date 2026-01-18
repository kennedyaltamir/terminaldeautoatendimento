# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 11:15:00
import os
import shutil
from pathlib import Path

def sanitize():
    print("🧹 Iniciando Faxina Final (Rito de Selagem Gold Master)...")
    
    ignore_base = Path("Limpando")
    ignore_base.mkdir(exist_ok=True)

    # 1. Pastas para Arquivamento Total
    folders_to_archive = [
        "comunication",
        "testesvisuais",
        "backups",
        "venv",
        "test-results"
    ]

    for folder in folders_to_archive:
        path = Path(folder)
        if path.exists():
            dest = ignore_base / folder
            if dest.exists(): shutil.rmtree(dest)
            try:
                shutil.move(str(path), str(dest))
                print(f"   [📦] Pasta arquivada: {folder}")
            except Exception as e:
                print(f"   [!] Erro ao mover {folder}: {e}")

    # 2. Arquivos de Rascunho e Backups de Ambiente
    files_to_archive = [
        "HANDOFF_MINIMAL.md",
        "MESAFLOW_OMNISCIENCE_PROTOCOL.md",
        "MIGRATION_PLAN_DRAFT.md",
        ".env.dev.backup",
        "kernel_journal.jsonl",
        "pytest.ini" # Move para scripts/tests se necessário, ou ignora
    ]

    archive_docs = ignore_base / "docs_archive"
    archive_docs.mkdir(exist_ok=True)

    for file in files_to_archive:
        path = Path(file)
        if path.exists():
            shutil.move(str(path), str(archive_docs / file))
            print(f"   [📄] Arquivo arquivado: {file}")

    # 3. Reset do Journal (Cria um novo limpo)
    with open("kernel_journal.jsonl", "w", encoding="utf-8") as f:
        f.write('{"event": "SYSTEM_SEALED", "status": "GOLD_MASTER", "timestamp": "2026-01-16T11:15:00Z"}\n')
    print("   [✨] Kernel Journal resetado e selado.")

    print("\n🏆 SISTEMA HIGIENIZADO COM SUCESSO.")
    print("Sua raiz agora reflete um projeto de Nível Industrial.")

if __name__ == "__main__":
    sanitize()