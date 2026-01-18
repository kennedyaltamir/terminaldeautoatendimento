# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 07:50:00
import os
import json
from pathlib import Path

# ==============================================================================
# 👻 GHOST CLEANUP UTILITY
# ==============================================================================
# Remove arquivos de documentação órfãos listados no relatório de cobertura.
# ==============================================================================

REPORT_FILE = Path("docs/audit/UI_COVERAGE_REPORT.md")
DOCS_ROOT = Path("doctelas")

def cleanup():
    print("👻 Iniciando limpeza de Ghosts...")
    
    if not REPORT_FILE.exists():
        print("❌ Relatório de cobertura não encontrado. Execute o auditor primeiro.")
        return

    content = REPORT_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    ghosts = []
    for line in lines:
        if "| GHOST" in line or "Remover Arquivo .md" in line:
            # Extrai nome da tela e plataforma da tabela Markdown
            # Ex: | 🟡 MÉDIA | AdminFranchisePage | web | Remover Arquivo .md (Órfão) |
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                name = parts[2]
                platform = parts[3]
                ghosts.append((name, platform))

    if not ghosts:
        print("✨ Nenhum Ghost detectado no relatório.")
        return

    removed_count = 0
    for name, platform in ghosts:
        filename = f"{name}.md"
        file_path = DOCS_ROOT / platform / filename
        
        if file_path.exists():
            try:
                os.remove(file_path)
                print(f"   🗑️  Removido: {platform}/{filename}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Erro ao remover {filename}: {e}")
        else:
            print(f"   ⚠️  Arquivo não encontrado (já removido?): {platform}/{filename}")

    print(f"\n✨ Limpeza concluída. {removed_count} arquivos removidos.")

if __name__ == "__main__":
    cleanup()

