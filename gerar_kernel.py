# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-08 00:55:00
# VERSION: 1.1
import os
from pathlib import Path
from datetime import datetime, timezone

# ==============================================================================
# CONFIGURAÇÃO DO GERADOR DE KERNEL COGNITIVO (KernelGen v1.1)
# ==============================================================================

OUTPUT_FILE = "governance_bundle.txt"

# Tags de encapsulamento protegidas
TAG_START = "[[" + "MESAFLOW_BEGIN:"
TAG_END = "[[" + "MESAFLOW_END]]"

# Lista Estrita de Ingestão (A "Constituição" e o "Bootloader")
KERNEL_FILES = [
    "docs/governance/AI_STARTUP_SEQUENCE.xml",
    "docs/Prompts/System_Persona.xml",
    "docs/governance/AI_ROLE_PROTOCOL.md",
    "docs/governance/AI_COGNITIVE_PROFILE.xml",
    "docs/governance/AI_COGNITIVE_PROFILE_LITE.xml",
    "docs/governance/FAIL_FAST_PROTOCOL.md",
    "docs/governance/ERROR_RESPONSE_MAPPING_PROTOCOL.md",
    "docs/governance/UPDATE_EXECUTION_PROTOCOL.md",
    "docs/governance/SECURITY_BOUNDARY_PROTOCOL.md",
]

def get_file_metadata(path_obj: Path) -> str:
    try:
        mtime = path_obj.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "UNKNOWN"

def main():
    print(f"🧬 Gerando Governance Kernel Bundle v1.1...")
    
    total_bytes = 0
    found_count = 0
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("<!-- MESAFLOW COGNITIVE KERNEL BUNDLE -->\n")
        out.write(f"<!-- GENERATED_AT: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC -->\n")
        out.write("<!-- INSTRUCTION: LEIA AI_STARTUP_SEQUENCE.XML PARA INICIAR O BOOT. -->\n\n")
        
        for rel_path in KERNEL_FILES:
            p = Path(rel_path)
            if p.exists():
                try:
                    last_mod = get_file_metadata(p)
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    
                    out.write(f"{TAG_START}{rel_path}]]\n")
                    out.write(f"# LAST_MODIFIED: {last_mod}\n")
                    out.write(content)
                    if not content.endswith("\n"): out.write("\n")
                    out.write(f"{TAG_END}\n\n")
                    
                    total_bytes += len(content.encode('utf-8'))
                    found_count += 1
                    print(f"   ✅ {rel_path}")
                except Exception as e:
                    print(f"   ❌ Erro em {rel_path}: {e}")
            else:
                print(f"   ⚠️  Arquivo ausente: {rel_path}")

    print(f"\n✨ Bundle gerado: {OUTPUT_FILE} ({total_bytes / 1024:.2f} KB)")

if __name__ == "__main__":
    main()