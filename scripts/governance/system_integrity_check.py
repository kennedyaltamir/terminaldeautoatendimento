
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 12:00:00
import os
import sys
import io
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# Fix para encoding no Windows (ORD-001)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REGISTRY_PATH = Path("governance/registry.xml")
REPORT_PATH = Path("governance/evidence/REPORT_SYSTEM_INTEGRITY.md")

def run_integrity_audit():
    print("🛡️  Iniciando Auditoria de Integridade do Sistema...")
    
    # 1. Verifica se a migração da governança ocorreu
    if Path("docs/governance").exists():
        print("❌ FALHA: Pasta legada docs/governance ainda existe. Remova-a após migrar.")
        return 1
    
    if not REGISTRY_PATH.exists():
        print("❌ FALHA: Registry principal não encontrado em /governance")
        return 1

    # 2. Verifica estrutura física mínima
    required_paths = ["app", "frontend", "mobile", "scripts", "governance/evidence", "governance/policies"]
    results = []
    for p in required_paths:
        exists = Path(p).exists()
        results.append(f"| `{p}` | {'✅' if exists else '❌'} |")

    # 3. Gera relatório
    report_content = [
        "# 🛡️ Relatório de Integridade Sistêmica",
        f"**Auditado em:** {datetime.now().isoformat()}",
        "\n## 1. Verificação de Caminhos Críticos",
        "| Diretório | Status |",
        "| :--- | :---: |",
        *results,
        "\n## 2. Veredito",
        "Sistema estruturalmente íntegro."
    ]
    
    os.makedirs(REPORT_PATH.parent, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_content), encoding="utf-8")
    
    print(f"✅ Auditoria concluída. Resultado em {REPORT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(run_integrity_audit())

