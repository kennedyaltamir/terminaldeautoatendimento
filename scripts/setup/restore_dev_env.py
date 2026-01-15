
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 13:15:00
import os
import shutil
from pathlib import Path

# ==============================================================================
# 🔄 RESTORE DEV ENVIRONMENT
# ==============================================================================
# Restaura o .env funcional a partir do backup criado pelo mock generator.
# ==============================================================================

ENV_PATH = Path(".env")
BACKUP_PATH = Path(".env.dev.backup")

def restore():
    print("🔄 Restoring Development Environment...")
    
    if BACKUP_PATH.exists():
        try:
            shutil.copy(BACKUP_PATH, ENV_PATH)
            print(f"   ✅ Restored .env from {BACKUP_PATH}")
        except Exception as e:
            print(f"   ❌ Failed to restore: {e}")
    else:
        print("   ⚠️  Backup not found. Creating default dev environment...")
        # Fallback seguro para dev local
        default_dev = """ENVIRONMENT=development
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mesaflow_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev_secret_key_change_me
STRIPE_SECRET_KEY=sk_test_placeholder
STRIPE_PRO_PRICE_ID=price_test_placeholder
STRIPE_WEBHOOK_SECRET=whsec_test_placeholder
MP_ACCESS_TOKEN=TEST-TOKEN-L7-PROD
MP_APP_ID=test_app_id
MP_CLIENT_SECRET=test_client_secret
IFOOD_WEBHOOK_SECRET=default_secret_change_me
IFOOD_CLIENT_ID=test_ifood_id
IFOOD_CLIENT_SECRET=test_ifood_secret
SENTRY_DSN_BACKEND=
NEXT_PUBLIC_SENTRY_DSN=
WHATSAPP_API_URL=http://localhost:8080
WHATSAPP_API_TOKEN=test_token
WHATSAPP_INSTANCE=MesaFlow_Dev
"""
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write(default_dev)
        print("   ✅ Created default local .env")

if __name__ == "__main__":
    restore()

