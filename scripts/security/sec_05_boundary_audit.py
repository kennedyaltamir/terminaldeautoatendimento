
import os
import sys
from pathlib import Path

# ==============================================================================
# 🛡️ SECURITY BOUNDARY AUDIT (SEC-05)
# ==============================================================================
# Objetivo: Verificar se os headers de segurança estão aplicados no entrypoint.
# Alvo: app/main.py
# ==============================================================================

TARGET_FILE = Path("app/main.py")
REPORT_PATH = Path("comunication/reports/REPORT_SEC_05.md")

REQUIRED_HEADERS = [
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Content-Security-Policy",
    "Permissions-Policy"
]

def audit_boundary():
    print("🛡️  Running SEC-05: Security Boundary Audit...")
    
    if not TARGET_FILE.exists():
        print(f"❌ Critical: {TARGET_FILE} not found.")
        return 1

    content = TARGET_FILE.read_text(encoding="utf-8")
    
    results = []
    missing = 0
    
    for header in REQUIRED_HEADERS:
        if header in content:
            results.append({"header": header, "status": "PRESENT"})
        else:
            results.append({"header": header, "status": "MISSING"})
            missing += 1

    # Generate Report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# 🛡️ Security Boundary Report (SEC-05)\n\n")
        f.write("## Header Analysis (app/main.py)\n")
        f.write("| Header | Status |\n")
        f.write("| :--- | :---: |\n")
        for r in results:
            icon = "✅" if r["status"] == "PRESENT" else "❌"
            f.write(f"| `{r['header']}` | {icon} {r['status']} |\n")
            
        f.write("\n## Veredito\n")
        if missing == 0:
            f.write("✅ **PASS:** A aplicação implementa Middleware de Segurança com todos os headers críticos.\n")
        else:
            f.write(f"❌ **FAIL:** Faltam {missing} headers de segurança obrigatórios.\n")

    if missing > 0:
        print(f"❌ Audit Failed: {missing} headers missing.")
        return 1
        
    print(f"✅ Audit Passed. Report: {REPORT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(audit_boundary())

