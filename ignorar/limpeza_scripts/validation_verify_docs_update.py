import os
import sys

def verify_docs():
    print("🔍 Verificando Atualização de Documentação...")

    # 1. Verificar Changelog
    changelog_path = "docs/CHANGELOG.md"
    if not os.path.exists(changelog_path):
        print(f"❌ Arquivo {changelog_path} não encontrado.")
        sys.exit(1)
    
    with open(changelog_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "[3.2.0]" not in content:
            print("❌ Versão 3.2.0 não encontrada no Changelog.")
            sys.exit(1)
        print("✅ Changelog atualizado com v3.2.0.")

    # 2. Verificar Troubleshooting
    troubleshoot_path = "docs/troubleshooting/TROUBLESHOOTING_MASTER.md"
    if not os.path.exists(troubleshoot_path):
        print(f"❌ Arquivo {troubleshoot_path} não encontrado.")
        sys.exit(1)

    with open(troubleshoot_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "TS-015" not in content or "MISSING_BOTO3" not in content:
            print("❌ Erro TS-015 (Boto3) não registrado no Troubleshooting.")
            sys.exit(1)
        if "TS-017" not in content or "SCA_VULN" not in content:
            print("❌ Erro TS-017 (SCA) não registrado no Troubleshooting.")
            sys.exit(1)
        print("✅ Troubleshooting Master Log atualizado.")

    print("\n🏆 Documentation Update Verified: All records are current.")
    sys.exit(0)

if __name__ == "__main__":
    verify_docs()
