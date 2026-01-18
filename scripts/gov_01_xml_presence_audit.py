
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-13 03:30:00
import os
import sys
from pathlib import Path

# ==============================================================================
# 🏛️ GOVERNANCE XML PRESENCE AUDIT (GOV-01)
# ==============================================================================
# Objetivo: Verificar a existência dos arquivos de governança sem criá-los.
# Regra: A IA não cria governança, apenas audita.
# ==============================================================================

GOV_DIR = Path("governance")
REQUIRED_FILES = [
    "architecture.xml",
    "business_rules.xml",
    "security_model.xml",
    "deployment_contract.xml"
]
REPORT_PATH = "comunication/reports/REPORT_GOV_01_XML_PRESENCE.md"

def audit_governance():
    print("🏛️  Running GOV-01: Governance XML Presence Audit...")
    
    results = []
    missing_count = 0
    
    if not GOV_DIR.exists():
        print("❌ Critical: /governance directory missing.")
        missing_count = len(REQUIRED_FILES)
        for f in REQUIRED_FILES:
            results.append({"file": f, "status": "MISSING"})
    else:
        for filename in REQUIRED_FILES:
            file_path = GOV_DIR / filename
            if file_path.exists() and file_path.stat().st_size > 0:
                results.append({"file": filename, "status": "PRESENT"})
            else:
                results.append({"file": filename, "status": "MISSING"})
                missing_count += 1

    # Gerar Relatório
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# 🏛️ Governance XML Audit Report (GOV-01)\n\n")
        f.write("## Status da Auditoria\n")
        f.write("| Arquivo | Status |\n")
        f.write("| :--- | :---: |\n")
        for r in results:
            icon = "✅" if r["status"] == "PRESENT" else "❌"
            f.write(f"| `{r['file']}` | {icon} {r['status']} |\n")
        
        f.write("\n## Veredito\n")
        if missing_count == 0:
            f.write("✅ **SUCCESS:** Todos os artefatos de governança estão presentes.\n")
        else:
            f.write(f"❌ **BLOCKED_BY_DATA:** Faltam {missing_count} arquivos de governança.\n")
            f.write("> **Ação Requerida:** O Auditor Humano deve fornecer ou autorizar a criação inicial destes arquivos.\n")

    if missing_count > 0:
        print(f"❌ Audit Failed: {missing_count} files missing. See {REPORT_PATH}")
        return 1
    
    print(f"✅ Audit Passed. See {REPORT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(audit_governance())

