# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 21:00:00
import os
import shutil
from pathlib import Path

# ==============================================================================
# CONFIGURAÇÃO DA PADRONIZAÇÃO
# ==============================================================================
BASE_DIR = Path("scripts")
TRASH_DIR = Path("ignorar/obsoletos")

# Mapa de Destino: Arquivo -> Pasta Correta dentro de scripts/
# Se o arquivo não estiver nesta lista, ele será movido para o lixo.
ALLOWED_SCRIPTS = {
    # Automation
    "enterprise_ui_explorer_v3.py": "automation",
    "map_routes.py": "automation",
    "auto_fix_reporter.py": "automation",
    
    # Maintenance
    "seed_ui_states.py": "maintenance",
    "system_integrity_check.py": "maintenance",
    "fix_tables_route.py": "maintenance",
    "standardize_scripts.py": "maintenance",
    "cleanup_context_noise.py": "maintenance", # Mantém os cleanups recentes
    "cleanup_scripts_noise.py": "maintenance",
    "cleanup_final_sweep.py": "maintenance",

    # Setup
    "audit_env.py": "setup",
    "setup_redis.py": "setup",
    
    # Tests (Unitários essenciais que sobraram)
    "conftest.py": "tests",
    "__init__.py": "tests"
}

# Arquivos na raiz do projeto que são scripts mas não ficam na pasta scripts/
ROOT_EXCEPTIONS = ["run.py", "atualizar.py", "gerartxt.py"]

def standardize():
    print("🗂️  Padronizando estrutura de Scripts (MesaFlow Standard)...")
    
    if not TRASH_DIR.exists():
        TRASH_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Criar subpastas oficiais se não existirem
    official_folders = set(ALLOWED_SCRIPTS.values())
    for folder in official_folders:
        (BASE_DIR / folder).mkdir(exist_ok=True)

    moved_to_trash = 0
    organized_count = 0

    # 2. Varrer a pasta scripts/ recursivamente
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            file_path = Path(root) / file
            
            # Ignora arquivos que não são scripts python/shell (ex: json, md)
            if file_path.suffix not in ['.py', '.sh', '.bat']:
                continue

            # Se o arquivo está na lista permitida
            if file in ALLOWED_SCRIPTS:
                target_folder = ALLOWED_SCRIPTS[file]
                target_path = BASE_DIR / target_folder / file
                
                # Se não está na pasta certa, move
                if file_path.resolve() != target_path.resolve():
                    try:
                        shutil.move(str(file_path), str(target_path))
                        print(f"   ✅ Organizado: {file} -> {target_folder}/")
                        organized_count += 1
                    except Exception as e:
                        print(f"   ❌ Erro ao organizar {file}: {e}")
            
            # Se NÃO está na lista permitida (e não é o próprio script rodando)
            elif file != "standardize_scripts.py":
                # Move para o lixo
                target_trash = TRASH_DIR / file
                try:
                    shutil.move(str(file_path), str(target_trash))
                    print(f"   🗑️  Obsoleto: {file} -> ignorar/obsoletos/")
                    moved_count += 1
                except Exception as e:
                    print(f"   ❌ Erro ao descartar {file}: {e}")

    # 3. Limpar pastas vazias em scripts/
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        for name in dirs:
            d = Path(root) / name
            if not any(d.iterdir()):
                d.rmdir()
                print(f"   🧹 Pasta vazia removida: {name}")

    print(f"\n✨ Padronização concluída.")
    print(f"   - Organizados: {organized_count}")
    print(f"   - Removidos (Obsoletos): {moved_to_trash}")
    print(f"   - Inventário Ativo: {len(ALLOWED_SCRIPTS)} scripts.")

if __name__ == "__main__":
    standardize()
