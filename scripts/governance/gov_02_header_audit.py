# DOMAIN: DEVOPS
# LAST_MODIFIED: 2026-01-13 02:35:00
import os
import sys
from pathlib import Path
def audit_headers():
    """
    GOV-02: Mandatory Header Audit (v2.1 - High Performance).
    Garante que todos os arquivos de código possuam o cabeçalho de domínio.
    Otimizado para ignorar pastas pesadas antes da listagem.
    """
    print("⚖️ Running GOV-02: Mandatory Header Audit (Optimized)...")
    extensions = {'.py', '.ts', '.tsx', '.xml'}
    ignored_dirs = {'node_modules', '.next', '.venv', 'backups', '.git', 'ignorar', '__pycache__', '.expo', '.mesaflow_cache'}
    violations = []
    total_checked = 0
    # os.walk com poda de diretórios é significativamente mais rápido que rglob
    for root, dirs, files in os.walk("."):
        # Modificar dirs in-place remove as pastas da recursão
        dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith('.')]
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in extensions:
                total_checked += 1
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        # Lê apenas o topo do arquivo para performance
                        content = f.read(500) 
                        if "DOMAIN:" not in content and "MESAFLOW_BEGIN" not in content:
                            violations.append(str(file_path))
                except:
                    continue
    report_path = "comunication/reports/REPORT_GOV_02.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# ⚖️ Header Integrity Audit (GOV-02)\n\n")
        f.write(f"- **Files Checked:** {total_checked}\n")
        f.write(f"- **Violations Found:** {len(violations)}\n\n")
        if violations:
            f.write("## 🚨 Files Missing Headers\n")
            for v in violations:
                f.write(f"- `{v}`\n")
            f.write("\n**Verdict:** ❌ FAIL\n")
        else:
            f.write("\n**Verdict:** ✅ PASS\n")
    print(f"✅ Header audit completed in sub-second. Report: {report_path}")
    return 1 if violations else 0
if __name__ == "__main__":
    sys.exit(audit_headers())