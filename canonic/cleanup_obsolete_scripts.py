# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 05:40:00
import os
import shutil
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🧹 SCRIPT CLEANUP UTILITY (L6 Hygiene)
# ==============================================================================
# Move scripts obsoletos, duplicados ou de uso único para a pasta 'ignorar/'.
# ==============================================================================

ROOT_DIR = Path(".")
TRASH_DIR = ROOT_DIR / "ignorar" / f"obsoletos_{datetime.now().strftime('%Y%m%d')}"

# Lista de arquivos para remover (Caminhos relativos à raiz)
TARGETS = [
    # Duplicatas (Mantendo versão canônica em outro lugar)
    "scripts/validar/master_readiness_check.py",
    "scripts/validar/otimizar.py",
    "scripts/validar/verify_TASK-SEC-01.py",
    "scripts/maintenance/system_integrity_check.py",
    "scripts/validar/reconcile_payments.py",
    "scripts/validar/seed.py",
    "scripts/validar/apply_rls_migrations.py",
    "scripts/validar/inspect_rls_context.py",
    "scripts/validar/verify_rls_policies_exist.py",
    "scripts/validar/verify_migrations_applied.py",
    
    # Stubs / Lixo em comunication/scripts
    "comunication/scripts/app_03_transaction_check.py",
    "comunication/scripts/app_04_error_handling.py",
    "comunication/scripts/bkp_02_snapshot_integrity.py",
    "comunication/scripts/data_integrity_scan.py",
    "comunication/scripts/data_orphan_detection.py",
    "comunication/scripts/obs_02_log_structure.py",
    "comunication/scripts/obs_03_correlation_id.py",
    "comunication/scripts/migrate_registry_enums_v10.py",

    # Scripts de Fix Único (Já aplicados)
    "scripts/automation/fix_inf_01.bat",
    "scripts/automation/fix_driver_loop.py",
    "scripts/automation/fix_driver_page_v2.py",
    "scripts/maintenance/fix_broken_links.py",
    "scripts/maintenance/fix_drift_evidence.py",
    "scripts/maintenance/fix_enum_drift.py",
    "scripts/maintenance/fix_migration_imports.py",
    "scripts/maintenance/fix_tables_route.py",
    "scripts/maintenance/fix_ts_header_syntax.py",
    "scripts/setup/fix_env_encoding.py",
    "scripts/setup/fix_frontend_deps.py",
    "scripts/setup/fix_local_redis.py",
    "scripts/setup/force_connect_redis.py",
    "scripts/setup/force_fix_env.py",
    "scripts/setup/force_redis_ip.py",
    "scripts/setup/force_redis_stable.py",
    "scripts/setup/patch_ifood_secret.py",
    "scripts/setup/restore_dev_env.py",
    "scripts/setup/smart_redis_setup.py",

    # Testes/Validações Antigos
    "scripts/tests/e2e_system_flow.py",
    "scripts/validar/enterprise_ui_explorer_v5_1.py",
    "scripts/verification/hyperoptimus_tables_check.py",
    "scripts/validation/verify_TASK-AI-01.py",
    "scripts/validation/verify_TASK-ESC-01.py"
]

def cleanup():
    print("🧹 Iniciando limpeza de scripts obsoletos...")
    
    if not TRASH_DIR.exists():
        TRASH_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📁 Diretório de lixo criado: {TRASH_DIR}")

    moved_count = 0
    not_found_count = 0

    for target in TARGETS:
        file_path = ROOT_DIR / target
        if file_path.exists():
            try:
                # Cria a estrutura de pastas no destino para manter organização
                dest_path = TRASH_DIR / target
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.move(str(file_path), str(dest_path))
                print(f"   🗑️  Movido: {target}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Erro ao mover {target}: {e}")
        else:
            not_found_count += 1
            # print(f"   ℹ️  Não encontrado (já limpo?): {target}")

    print("-" * 50)
    print(f"🏁 Limpeza concluída.")
    print(f"   - Scripts movidos: {moved_count}")
    print(f"   - Scripts não encontrados: {not_found_count}")
    print(f"   - Localização: {TRASH_DIR}")

    # Remove diretórios vazios em scripts/validar e comunication/scripts se sobrarem
    for d in ["scripts/validar", "comunication/scripts"]:
        dir_path = ROOT_DIR / d
        if dir_path.exists() and not any(dir_path.iterdir()):
            try:
                dir_path.rmdir()
                print(f"   🧹 Diretório vazio removido: {d}")
            except: pass

if __name__ == "__main__":
    cleanup()

