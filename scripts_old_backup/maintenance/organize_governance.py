
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 12:40:00
import os
import shutil
from pathlib import Path

def organize():
    print("🧹 Iniciando normalização da Governança MesaFlow...")
    
    root_gov = Path("governance")
    nested_gov = root_gov / "governance"
    
    if not nested_gov.exists():
        print("✅ Pasta redundante não encontrada. O sistema já está limpo.")
        return

    # 1. Criar pasta RFC oficial
    rfc_dir = root_gov / "rfc"
    rfc_dir.mkdir(exist_ok=True)
    
    # 2. Mover RFCs de todos os locais para a pasta oficial
    rfc_sources = [nested_gov / "RFC", nested_gov]
    for src in rfc_sources:
        if src.exists():
            for f in src.glob("RFC-*.md"):
                shutil.move(str(f), str(rfc_dir / f.name))
            for f in src.glob("*.md"):
                if f.name.startswith("RFC"):
                    shutil.move(str(f), str(rfc_dir / f.name))

    # 3. Mover Policies
    policy_dest = root_gov / "policies"
    policy_dest.mkdir(exist_ok=True)
    if (nested_gov / "policies").exists():
        for f in (nested_gov / "policies").glob("*.md"):
            shutil.move(str(f), str(policy_dest / f.name))

    # 4. Mover protocolos e specs para a raiz da governança
    for f in nested_gov.glob("*.*"):
        if f.is_file() and f.name not in ["README.md"]:
            shutil.move(str(f), str(root_gov / f.name))

    # 5. Remover a pasta redundante
    shutil.rmtree(str(nested_gov))
    print("✨ Governança normalizada com sucesso!")

if __name__ == "__main__":
    organize()

