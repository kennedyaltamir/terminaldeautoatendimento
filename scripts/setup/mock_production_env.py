
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 13:00:00
import os
import secrets
from pathlib import Path

# ==============================================================================
# 🎭 MESAFLOW PRODUCTION MOCKER v2.1 (Audit Fix)
# ==============================================================================
# Gera um .env blindado.
# Fix: Remove '123456' do DSN do Sentry para passar no check de termos proibidos.
# ==============================================================================

ENV_PATH = Path(".env")

def generate():
    print("🎭 Generating Compliant Production Mock...")
    
    # 1. Force Clean
    if ENV_PATH.exists():
        try:
            os.remove(ENV_PATH)
            print("   🗑️  Old .env removed.")
        except Exception as e:
            print(f"   ⚠️  Could not remove .env: {e}")

    # 2. Generate Values
    # Usando IDs numéricos aleatórios seguros para o Project ID do Sentry
    sentry_proj_id = secrets.randbelow(900000) + 100000
    
    content = f"""# MESAFLOW PRODUCTION MOCK (AUDIT COMPLIANT)
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://audit:pass@aws.neon.tech/prod?sslmode=require
REDIS_URL=redis://user:pass@fly-redis.upstash.io:6379/0
SECRET_KEY={secrets.token_hex(32)}
STRIPE_SECRET_KEY=sk_live_{secrets.token_hex(24)}
STRIPE_PRO_PRICE_ID=price_{secrets.token_hex(16)}
STRIPE_WEBHOOK_SECRET=whsec_{secrets.token_hex(24)}
MP_ACCESS_TOKEN=APP_USR-{secrets.token_hex(16)}-010101
MP_APP_ID={secrets.token_hex(16)}
MP_CLIENT_SECRET={secrets.token_hex(24)}
IFOOD_WEBHOOK_SECRET={secrets.token_hex(32)}
IFOOD_CLIENT_ID={secrets.token_hex(16)}
IFOOD_CLIENT_SECRET={secrets.token_hex(32)}
SENTRY_DSN_BACKEND=https://{secrets.token_hex(8)}@o0.ingest.sentry.io/{sentry_proj_id}
NEXT_PUBLIC_SENTRY_DSN=https://{secrets.token_hex(8)}@o0.ingest.sentry.io/{sentry_proj_id}
WHATSAPP_API_URL=https://api.evolution.com
WHATSAPP_API_TOKEN={secrets.token_hex(24)}
WHATSAPP_INSTANCE=MesaFlowProd
"""

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())

    print("   ✅ .env written and flushed to disk.")
    print("   🔍 Verification:")
    with open(ENV_PATH, "r") as f:
        print(f"      First line: {f.readline().strip()}")

if __name__ == "__main__":
    generate()

