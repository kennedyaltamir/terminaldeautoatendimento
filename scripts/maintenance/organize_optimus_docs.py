import os
import shutil
from pathlib import Path

# Configuração
DOCS_DIR = Path("docs")
ARCHIVE_DIR = DOCS_DIR / "archive" / "legacy_optimus"
TASKS_DIR = DOCS_DIR / "tasks"
REPORTS_DIR = DOCS_DIR / "reports"
GOVERNANCE_DIR = DOCS_DIR / "governance"

# Arquivos para Arquivar (Obsoletos)
FILES_TO_ARCHIVE = [
    # Planos Antigos
    GOVERNANCE_DIR / "HYPEROPTIMUS_PLAN.md",
    GOVERNANCE_DIR / "HYPEROPTIMUS_PLAN_V4.md",
    
    # Relatórios Antigos
    REPORTS_DIR / "OPTIMUS_V5_VS_V7_COMPARISON.md",
    REPORTS_DIR / "V7_TO_V8_UPGRADE_LOG.md",
    
    # Tasks de Versões Anteriores
    TASKS_DIR / "TASK-AUTO-03_OPTIMUS_VISUAL_TESTER.md",
    TASKS_DIR / "TASK-AUTO-04_OPTIMUS_V7.md",
    TASKS_DIR / "TASK-AUTO-05_GENOME_TESTER.md",
    TASKS_DIR / "TASK-AUTO-06_OPTIMUS_V8.md",
    TASKS_DIR / "TASK-AUTO-07_OPTIMUS_V8_1.md",
    TASKS_DIR / "TASK-AUTO-08_OPTIMUS_V8_2.md"
]

def organize_docs():
    print("🧹 Organizando Documentação do Optimus...")
    
    if not ARCHIVE_DIR.exists():
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📁 Diretório de arquivo criado: {ARCHIVE_DIR}")

    moved_count = 0
    
    for file_path in FILES_TO_ARCHIVE:
        if file_path.exists():
            target_path = ARCHIVE_DIR / file_path.name
            try:
                shutil.move(str(file_path), str(target_path))
                print(f"   📦 Arquivado: {file_path.name}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Erro ao arquivar {file_path.name}: {e}")
        else:
            print(f"   ⚠️  Arquivo não encontrado (já movido?): {file_path.name}")

    print(f"\n✨ Organização concluída. {moved_count} arquivos movidos para {ARCHIVE_DIR}.")
    print("   O arquivo 'docs/governance/OPTIMUS_v9_Architecture.md' permanece como SSOT.")

if __name__ == "__main__":
    organize_docs()