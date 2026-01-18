# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-16 10:45:00
import os
import sys
import io
from pathlib import Path
from datetime import datetime

# Fix para encoding no Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REPORT_PATH = Path("governance/evidence/REPORT_SYSTEM_INTEGRITY.md")

def run_integrity_audit():
    print("🛡️  Iniciando Auditoria de Integridade Estrutural v2.0...")
    
    # 1. Verificação de Pastas Legadas (Não podem existir na raiz para evitar confusão de SSOT)
    legacy_folders = ["docs/governance", "comunication/scripts"]
    for legacy in legacy_folders:
        if Path(legacy).exists():
            print(f"❌ FALHA: Pasta legada '{legacy}' detectada. Mova para /ignorar.")
            return 1

    # 2. Verificação de Estrutura Canônica L6
    # Adicionada a pasta 'canonic' como obrigatória para o novo motor de auditoria
    required_paths = [
        "app", 
        "frontend", 
        "mobile", 
        "scripts", 
        "canonic", 
        "governance/evidence", 
        "governance/policies"
    ]
    
    results = []
    all_present = True
    for p in required_paths:
        exists = Path(p).exists()
        if not exists: all_present = False
        results.append(f"| `{p}` | {'✅ PASS' if exists else '❌ MISSING'} |")

    # 3. Geração do Relatório de Evidência
    report_content = [
        "# 🛡️ Relatório de Integridade Sistêmica (SYS-01)",
        f"**Auditado em:** {datetime.now().isoformat()}",
        "\n## 1. Verificação de Caminhos Críticos",
        "| Diretório | Status |",
        "| :--- | :---: |",
        *results,
        "\n## 2. Veredito",
        "✅ **PASS**" if all_present else "❌ **FAIL**"
    ]
    
    os.makedirs(REPORT_PATH.parent, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_content), encoding="utf-8")
    
    if all_present:
        print("✅ Estrutura validada com sucesso.")
        return 0
    else:
        print("❌ Falha: Alguns diretórios críticos estão ausentes.")
        return 1

if __name__ == "__main__":
    sys.exit(run_integrity_audit())

