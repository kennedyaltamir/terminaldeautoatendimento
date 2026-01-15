# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:30:00
import os
import shutil
import sys
import io
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================================
# 🚚 CANONICAL MIGRATOR (L6 Realignment)
# ==============================================================================
# Move scripts da pasta legada /comunication/scripts para /scripts/<category>
# ==============================================================================

MAPPING = {
    "gov_01_xml_presence_audit.py": "governance",
    "gov_02_header_audit.py": "governance",
    "gov_03_schema_validation.py": "governance",
    "gov_04_registry_drift.py": "governance",
    "inf_01_healthcheck.py": "governance",
    "render_health_probe.py": "observability",
    "vercel_latency_check.py": "observability",
    "sentry_ingest_test.py": "observability",
    "expo_runtime_probe.py": "mobile",
    "sec_01A_rls_policy_inventory.py": "security",
    "sec_01B_rls_role_matrix.py": "security",
    "sec_01C_rls_effective_context.py": "security",
    "sec_01D_rls_readonly_probe.py": "security",
    "sec_01_rls_integrity.py": "security",
    "sec_04_env_audit.py": "security",
    "sec_05_boundary_audit.py": "security",
    "app_01_orm_context_sync.py": "validation",
    "app_02_idempotency_validation.py": "validation",
    "data_readiness_check.py": "validation",
}

def migrate():
    src_dir = Path("comunication/scripts")
    dest_root = Path("scripts")
    
    if not src_dir.exists():
        print("✅ Pasta legada já removida ou inexistente.")
        return

    print("🚚 Iniciando Migração Canônica...")
    for filename, category in MAPPING.items():
        src = src_dir / filename
        if src.exists():
            dest_dir = dest_root / category
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / filename
            
            try:
                shutil.move(str(src), str(dest))
                print(f"   [OK] {filename} -> scripts/{category}/")
            except Exception as e:
                print(f"   [ERR] Falha ao mover {filename}: {e}")

    # Limpeza da pasta antiga se estiver vazia
    try:
        if not any(src_dir.iterdir()):
            src_dir.rmdir()
            print("🧹 Pasta legada comunication/scripts removida.")
    except: pass

if __name__ == "__main__":
    migrate()
