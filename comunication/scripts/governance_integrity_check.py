# DOMAIN: DEVOPS
# LAST_MODIFIED: 2026-01-13 02:30:00
import os
import sys
import hashlib
def check_governance():
    """
    GOV-01: Governance Integrity Check.
    Valida a existência e o formato dos arquivos XML de governança.
    """
    gov_dir = "governance"
    required = ["architecture.xml", "business_rules.xml", "security_model.xml", "deployment_contract.xml"]
    print("⚖️ Checking Governance Integrity...")
    results = []
    all_ok = True
    if not os.path.exists(gov_dir):
        print("❌ /governance directory missing!")
        return 1
    for xml in required:
        path = os.path.join(gov_dir, xml)
        exists = os.path.exists(path)
        is_xml = False
        if exists:
            with open(path, 'r') as f:
                content = f.read().strip()
                is_xml = content.startswith('<') and content.endswith('>')
        if not exists or not is_xml: all_ok = False
        results.append({"file": xml, "exists": exists, "valid_xml": is_xml})
    report_path = "comunication/reports/REPORT_GOV_01.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# ⚖️ Governance Integrity Report (GOV-01)\n\n")
        for r in results:
            f.write(f"- **{r['file']}**: Exists: {r['exists']}, XML: {r['valid_xml']}\n")
    return 0 if all_ok else 1
if __name__ == "__main__":
    sys.exit(check_governance())