# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 06:00:00
import os
import shutil
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🧹 DOCS CLEANUP UTILITY (L6 Hygiene)
# ==============================================================================
# Move documentos obsoletos, duplicados ou de uso único para a pasta 'ignorar/'.
# ==============================================================================

ROOT_DIR = Path(".")
TRASH_DIR = ROOT_DIR / "ignorar" / f"docs_obsoletos_{datetime.now().strftime('%Y%m%d')}"

# Lista de arquivos para remover (Caminhos relativos à raiz)
TARGETS = [
    # Duplicatas / Redundantes
    "docs/Prompts/GO_LIVE_FINAL_PROMPT.md",
    "governance/protocols/GOVERNANCE_CHANGE_PROTOCOL.md",
    "docs/MANUAL_GARCOM.md",
    "docs/Projeto MesaFlow Corporate.md",
    "docs/legal/SLA_AGREEMENT.md",
    "docs/management/RACI_MATRIX.md",
    "docs/commercial/SALES_PLAYBOOK.md",
    "docs/commercial/ONBOARDING_CHECKLIST.md",
    "docs/DEEP_AUDIT_REPORT.md",
    "docs/MIGRATION_PLAN_DRAFT.md",
    "docs/ARCHITECTURAL_DECISIONS.md",

    # Stubs (Conteúdo vazio ou genérico)
    "docs/quality/QUALITY_METRICS.md",
    "docs/sre/RUNBOOK_DATABASE_FAILOVER.md",
    "docs/sre/RUNBOOK_REDIS_OUTAGE.md",
    "docs/sre/INCIDENT_RESPONSE_PLAN.md",
    "docs/integration/PARTNER_GUIDE.md",
    "docs/integration/WEBHOOK_SECURITY.md",

    # Logs de Tasks Antigas
    "docs/mobile/tasks/mobile_039_completion.md",
    "docs/mobile/tasks/mobile_040_completion.md",
    "docs/mobile/tasks/mobile_041_completion.md",
    "docs/mobile/tasks/mobile_14b_completion.md",
    "docs/mobile/tasks/fix_web_blank_screen.md",
    "docs/mobile/tasks/fix_web_import_meta.md",

    # Relatórios Antigos
    "docs/ROUTE_TEST_REPORT.md",
    "docs/SECURITY_AUDIT_REPORT.md",
    "docs/specs/UX_AUDIT_REPORT.md",
    "docs/specs/AUDIT_REPORT_V1.md",
    "docs/AUDIT_REPORT_2026-01.md",
    "docs/IMPLEMENTATION_LOG.md",
    "docs/IMPLEMENTATION_LOG_PHASE_7.md"
]

def cleanup():
    print("🧹 Iniciando limpeza de documentação obsoleta...")
    
    if not TRASH_DIR.exists():
        TRASH_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📁 Diretório de lixo criado: {TRASH_DIR}")

    moved_count = 0
    not_found_count = 0

    for target in TARGETS:
        file_path = ROOT_DIR / target
        if file_path.exists():
            try:
                # Cria a estrutura de pastas no destino para manter organização
                dest_path = TRASH_DIR / target
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.move(str(file_path), str(dest_path))
                print(f"   🗑️  Movido: {target}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Erro ao mover {target}: {e}")
        else:
            not_found_count += 1
            # print(f"   ℹ️  Não encontrado (já limpo?): {target}")

    print("-" * 50)
    print(f"🏁 Limpeza concluída.")
    print(f"   - Documentos movidos: {moved_count}")
    print(f"   - Documentos não encontrados: {not_found_count}")
    print(f"   - Localização: {TRASH_DIR}")

if __name__ == "__main__":
    cleanup()

