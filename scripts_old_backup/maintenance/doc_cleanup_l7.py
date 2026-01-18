# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 19:30:00
import os
import shutil
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🧹 DOCUMENTATION JANITOR L7
# ==============================================================================
# Move documentação obsoleta e logs antigos para a pasta 'ignorar/_archive'.
# Mantém apenas a "Constituição" e o estado atual.
# ==============================================================================

ARCHIVE_ROOT = Path("ignorar/_archive")
TIMESTAMP = datetime.now().strftime("%Y%m%d")

TARGETS_TO_MOVE = [
    # Pastas inteiras
    Path("docs/archive"),
    Path("docs/implemented"),
    Path("comunication/logs"),
    
    # Arquivos específicos (Versões obsoletas)
    Path("governance/evidence/REPORT_FINAL_STATUS.md"),
    Path("governance/evidence/REPORT_FINAL_STATUS_v2.md"),
]

def cleanup():
    print("🧹 Iniciando Limpeza de Documentação (L7 Standard)...")
    
    if not ARCHIVE_ROOT.exists():
        ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)

    moved_count = 0

    for target in TARGETS_TO_MOVE:
        if target.exists():
            dest_name = f"{target.name}_{TIMESTAMP}"
            dest_path = ARCHIVE_ROOT / dest_name
            
            try:
                # Se for diretório, move a árvore
                if target.is_dir():
                    # Se já existe no destino, remove para substituir (ou renomeia)
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.move(str(target), str(dest_path))
                    print(f"   📦 Pasta arquivada: {target} -> {dest_path}")
                
                # Se for arquivo
                elif target.is_file():
                    shutil.move(str(target), str(dest_path))
                    print(f"   📄 Arquivo arquivado: {target} -> {dest_path}")
                
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Erro ao mover {target}: {e}")
        else:
            print(f"   ℹ️  Alvo não encontrado (já limpo?): {target}")

    print("-" * 50)
    print(f"✨ Limpeza concluída. {moved_count} itens movidos para '{ARCHIVE_ROOT}'.")

if __name__ == "__main__":
    cleanup()

