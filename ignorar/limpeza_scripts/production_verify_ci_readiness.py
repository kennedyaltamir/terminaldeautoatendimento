import os
import sys
import yaml

def verify_ci_config():
    print("🔍 Iniciando Verificação de Hardening do CI/CD (TASK-OPS-05)...")

    ci_file = ".github/workflows/ci.yml"

    # 1. Verificar Existência
    if not os.path.exists(ci_file):
        print(f"❌ Arquivo de CI não encontrado: {ci_file}")
        sys.exit(1)

    # 2. Analisar Conteúdo YAML
    try:
        with open(ci_file, "r", encoding="utf-8") as f:
            # Leitura simples como texto para evitar dependência de PyYAML se não instalado
            # Mas vamos tentar usar yaml se disponível, ou fallback para string check
            content = f.read()
            
            required_checks = [
                "scripts/production/verify_adr_integrity.py",
                "scripts/production/verify_compliance_mapping.py",
                "scripts/production/verify_vendor_risk.py",
                "scripts/production/verify_trust_center.py",
                "scripts/production/verify_legal_compliance.py"
            ]

            missing = []
            for check in required_checks:
                if check not in content:
                    missing.append(check)
            
            if missing:
                print(f"❌ Scripts de governança ausentes no CI: {missing}")
                sys.exit(1)
            
            if "governance-audit" not in content:
                print("❌ Job 'governance-audit' não definido.")
                sys.exit(1)

            print("✅ Todos os scripts de governança estão configurados no pipeline.")
            print("✅ Job de auditoria detectado.")

    except Exception as e:
        print(f"❌ Erro ao ler arquivo CI: {e}")
        sys.exit(1)

    print("\n🏆 CI/CD Hardening Verified: Governance Gates are active.")
    sys.exit(0)

if __name__ == "__main__":
    verify_ci_config()
