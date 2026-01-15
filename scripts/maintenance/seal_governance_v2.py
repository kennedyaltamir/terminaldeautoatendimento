
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 13:00:00
import os
import shutil
from pathlib import Path

def seal():
    print("🛡️ Selando estrutura de Governança v2...")
    gov = Path("governance")
    
    # 1. Organizar Prompts/Perfis
    prompts_dir = gov / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    for f in gov.glob("AI_*.xml"):
        shutil.move(str(f), str(prompts_dir / f.name))
    if (gov / "AI_STARTUP_SEQUENCE.xml").exists():
        shutil.move(str(gov / "AI_STARTUP_SEQUENCE.xml"), str(prompts_dir / "AI_STARTUP_SEQUENCE.xml"))

    # 2. Consolidar RFCs (Mantendo apenas o padrão numérico)
    rfc_dir = gov / "rfc"
    for f in rfc_dir.glob("RFC-*_*.md"):
        print(f"   🗑️ Removendo duplicata descritiva: {f.name}")
        f.unlink()

    # 3. Mover Protocolos soltos para subpasta específica
    prot_dir = gov / "protocols"
    prot_dir.mkdir(exist_ok=True)
    for f in gov.glob("*_PROTOCOL.md"):
        shutil.move(str(f), str(prot_dir / f.name))
    
    print("✨ Governança selada e pronta para Auditoria L6.")

if __name__ == "__main__":
    seal()

