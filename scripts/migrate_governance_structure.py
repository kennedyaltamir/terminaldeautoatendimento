
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 11:40:00
import os
import shutil
from pathlib import Path

# ==============================================================================
# 🏗️ GOVERNANCE MIGRATOR v4.0
# ==============================================================================
# Transfere evidências do local antigo para a nova estrutura de governança.
# ==============================================================================

OLD_EVIDENCE_DIR = Path("comunication/reports")
NEW_EVIDENCE_DIR = Path("governance/evidence")
OLD_REGISTRY = Path("comunication/registry.xml")

def migrate():
    print("🏗️  Iniciando Migração Estrutural de Governança...")
    
    # 1. Criar pasta de evidências
    NEW_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 2. Mover relatórios existentes
    if OLD_EVIDENCE_DIR.exists():
        for report in OLD_EVIDENCE_DIR.glob("*.md"):
            dest = NEW_EVIDENCE_DIR / report.name
            try:
                shutil.move(str(report), str(dest))
                print(f"   📦 Evidência movida: {report.name}")
            except Exception as e:
                print(f"   ❌ Falha ao mover {report.name}: {e}")

    # 3. Mover RLS_VALIDATION se estiver na raiz ou pasta antiga
    rls_report = Path("comunication/reports/RLS_VALIDATION_REPORT.md")
    if rls_report.exists():
        shutil.move(str(rls_report), NEW_EVIDENCE_DIR / "RLS_VALIDATION_REPORT.md")

    # 4. Limpeza de pastas obsoletas
    if OLD_REGISTRY.exists():
        os.remove(OLD_REGISTRY)
        print("   🗑️  Registro antigo removido.")
    
    print("✅ Migração concluída. O sistema agora opera sob o padrão /governance.")

if __name__ == "__main__":
    migrate()

