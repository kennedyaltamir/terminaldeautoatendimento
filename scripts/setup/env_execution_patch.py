
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 12:05:00
import os
import sys
from pathlib import Path

# ==============================================================================
# 🌉 ENV EXECUTION PATCH v1.2 — Password Aware
# ==============================================================================

ENV_PATH = Path(".env")

def patch():
    if not ENV_PATH.exists():
        print("Error: .env not found.")
        return

    # Se você sabe que sua senha local é diferente de 'postgres', 
    # altere aqui ou passe como argumento.
    db_pass = sys.argv[1] if len(sys.argv) > 1 else "postgres"
    
    content = ENV_PATH.read_text(encoding='utf-8')
    lines = content.splitlines()
    new_lines = []
    
    for line in lines:
        if line.startswith("DATABASE_URL="):
            new_lines.append(f"DATABASE_URL=postgresql://postgres:{db_pass}@localhost:5432/mesaflow_db?sslmode=disable")
        elif line.startswith("ENVIRONMENT="):
            new_lines.append("ENVIRONMENT=staging")
        else:
            new_lines.append(line)
            
    ENV_PATH.write_text("\n".join(new_lines), encoding='utf-8')
    print(f"Success: .env patched for localhost with password: {db_pass}")

if __name__ == "__main__":
    patch()

