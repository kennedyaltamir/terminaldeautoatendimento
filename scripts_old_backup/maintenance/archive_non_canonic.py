import os
import shutil
from pathlib import Path

# ==============================================================================
# 🧹 ARCHIVE NON-CANONIC SCRIPTS
# ==============================================================================
# Objetivo: Mover scripts que não passaram no filtro para a pasta de ignorados.
# ==============================================================================

SOURCE_DIR = Path("scripts")
CANONIC_DIR = Path("canonic")
ARCHIVE_DIR = Path("ignorar/obsoletos_automacao")

# Scripts essenciais que nunca devem ser movidos (Infraestrutura)
PROTECTED_LIST = [
    "run.py",
    "setup_redis.py",
    "launch.bat",
    "dev.bat",
    "atualizar.py",
    "gerartxt.py",
    "archive_non_canonic.py",
    "the_great_filter.py",
    "finalize_canonic_protocol.py",
    "consolidate_filter_results.py"
]

def archive_scripts():
    print(f"🚀 Iniciando arquivamento de scripts não-canônicos...")
    
    if not ARCHIVE_DIR.exists():
        ARCHIVE_DIR.mkdir(parents=True)

    # 1. Listar scripts canônicos (Elite)
    canonic_names = {f.name for f in CANONIC_DIR.glob("*.py")}
    
    # 2. Varrer scripts originais
    moved_count = 0
    for script_path in SOURCE_DIR.rglob("*.py"):
        # Ignorar pastas especiais
        if "maintenance" in str(script_path) or "canonic" in str(script_path):
            continue
            
        script_name = script_path.name
        
        # Se não for canônico e não for protegido -> Arquivar
        if script_name not in canonic_names and script_name not in PROTECTED_LIST:
            try:
                dest_path = ARCHIVE_DIR / script_name
                shutil.move(str(script_path), str(dest_path))
                print(f"📦 Arquivado: {script_name}")
                moved_count += 1
            except Exception as e:
                print(f"⚠️ Erro ao mover {script_name}: {e}")

    print("\n" + "="*40)
    print(f"✅ Limpeza concluída!")
    print(f"📦 Scripts movidos para arquivo morto: {moved_count}")
    print(f"🛡️ Scripts canônicos mantidos: {len(canonic_names)}")
    print("="*40)

if __name__ == "__main__":
    archive_scripts()

