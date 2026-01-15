
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 14:05:00
import os
import sys
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ==============================================================================
# 🛡️ PRODUCTION ENV AUDITOR v3.7 (Environment Aware)
# ==============================================================================

REQUIRED_VARS = {
    "ENVIRONMENT": ["production", "development", "staging"],
    "DATABASE_URL": "sslmode=",
    "SECRET_KEY": None,
    "STRIPE_SECRET_KEY": "sk_",
    "MP_ACCESS_TOKEN": "APP_USR-",
    "SENTRY_DSN_BACKEND": "ingest.sentry.io"
}

FORBIDDEN_TERMS = ["changeme", "placeholder", "sua_chave_aqui"]

def run_audit():
    env_path = Path(".env")
    if not env_path.exists(): return 1

    errors = []
    current_env = os.getenv("ENVIRONMENT", "development")

    for var, constraint in REQUIRED_VARS.items():
        val = os.getenv(var)
        if not val:
            errors.append(f"MISSING: {var}")
            continue
        
        for term in FORBIDDEN_TERMS:
            if term in val.lower():
                errors.append(f"UNSAFE: {var} contém valor proibido '{term}'")

        # Validação específica para PRODUÇÃO
        if current_env == "production" and constraint:
            if isinstance(constraint, list):
                if val not in constraint:
                    errors.append(f"INVALID: {var}='{val}' não permitido em produção.")
            else:
                # Exigência de SSL em produção
                if var == "DATABASE_URL" and "sslmode=require" not in val:
                    errors.append(f"SECURITY: DATABASE_URL deve usar sslmode=require em produção.")
                elif var != "DATABASE_URL" and constraint not in val:
                    errors.append(f"INVALID: {var} deve conter assinatura '{constraint}'")

    # Write Report
    report_path = Path("governance/evidence/REPORT_SEC_04.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 🛡️ Secrets & Env Audit Report (SEC-04)\n\n")
        f.write(f"**Ambiente:** `{current_env}` | **Status:** {'❌ FAIL' if errors else '✅ PASS'}\n\n")
        if errors:
            for err in errors: f.write(f"- {err}\n")
        else:
            f.write("Ambiente validado e seguro para o nível atual.")
    
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(run_audit())

