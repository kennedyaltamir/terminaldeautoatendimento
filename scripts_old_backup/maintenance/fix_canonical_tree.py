# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 10:55:00
import os
import shutil
from pathlib import Path

def align():
    print("🏗️  Alinhando Estrutura Física ao Padrão Gold Master...")
    
    # 1. Definição de Pastas Obrigatórias
    folders = [
        "governance/evidence",
        "governance/policies",
        "governance/protocols",
        "governance/rfc",
        "scripts/governance",
        "scripts/validation",
        "scripts/maintenance",
        "scripts/security",
        "scripts/observability"
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"   [+] Pasta garantida: {folder}")

    # 2. Movimentação de Protocolos (MDs da raiz de governance para /protocols)
    gov_root = Path("governance")
    for md_file in gov_root.glob("*.md"):
        if md_file.name != "README.md":
            dest = gov_root / "protocols" / md_file.name
            shutil.move(str(md_file), str(dest))
            print(f"   [➔] Protocolo movido: {md_file.name}")

    # 3. Organização de Scripts (Raiz de scripts para subpastas)
    scripts_root = Path("scripts")
    
    # Mapeamento de Destino
    move_map = {
        "governance_integrity_check.py": "governance/system_integrity_check.py", # Renomeia para o padrão
        "inv_01_zero_config.py": "governance/inv_01_zero_config.py",
        "inv_02_readiness_summary.py": "governance/inv_02_readiness_summary.py",
        "inv_03_auditor_simulation.py": "governance/inv_03_auditor_simulation.py",
        "backup_diff_audit.py": "governance/backup_diff_audit.py",
        "ops_01_cognitive_prune.py": "governance/ops_01_cognitive_prune.py"
    }

    for src_name, dest_rel_path in move_map.items():
        src_path = scripts_root / src_name
        if src_path.exists():
            dest_path = scripts_root / dest_rel_path
            shutil.move(str(src_path), str(dest_path))
            print(f"   [➔] Script organizado: {src_name} -> {dest_rel_path}")

    print("\n✨ Estrutura alinhada com sucesso.")
    print("👉 Próximo passo: Execute o 'master_readiness_check.py' novamente.")

if __name__ == "__main__":
    align()

