
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-13 04:15:00
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# ==============================================================================
# 🏛️ GOVERNANCE XML SCHEMA VALIDATION (GOV-03)
# ==============================================================================
# Objetivo: Validar se os arquivos XML de governança são sintaticamente válidos.
# Critério: Well-formed XML (ElementTree parseable).
# ==============================================================================

GOV_DIR = Path("governance")
REPORT_PATH = "comunication/reports/REPORT_GOV_03.md"

def validate_schemas():
    print("🏛️  Running GOV-03: Governance XML Schema Validation...")
    
    if not GOV_DIR.exists():
        print("❌ Critical: /governance directory missing.")
        return 1

    results = []
    failures = 0
    
    xml_files = list(GOV_DIR.glob("*.xml"))
    if not xml_files:
        print("⚠️  No XML files found in governance directory.")
        return 1

    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            results.append({"file": xml_file.name, "status": "VALID", "details": "Well-formed XML"})
        except ET.ParseError as e:
            results.append({"file": xml_file.name, "status": "INVALID", "details": str(e)})
            failures += 1
        except Exception as e:
            results.append({"file": xml_file.name, "status": "ERROR", "details": str(e)})
            failures += 1

    # Gerar Relatório
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# 🏛️ Governance Schema Validation Report (GOV-03)\n\n")
        f.write("## Status da Validação\n")
        f.write("| Arquivo | Status | Detalhes |\n")
        f.write("| :--- | :---: | :--- |\n")
        for r in results:
            icon = "✅" if r["status"] == "VALID" else "❌"
            f.write(f"| `{r['file']}` | {icon} {r['status']} | `{r['details']}` |\n")
        
        f.write("\n## Veredito\n")
        if failures == 0:
            f.write("✅ **SUCCESS:** Todos os arquivos de governança são XMLs válidos.\n")
        else:
            f.write(f"❌ **FAILED:** {failures} arquivos corrompidos ou inválidos.\n")
            f.write("> **Ação Requerida:** Corrigir a sintaxe XML dos arquivos listados.\n")

    if failures > 0:
        print(f"❌ Validation Failed: {failures} invalid files. See {REPORT_PATH}")
        return 1
    
    print(f"✅ Validation Passed. See {REPORT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(validate_schemas())

