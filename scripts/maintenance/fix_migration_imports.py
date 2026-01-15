
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 00:30:00
import os
from pathlib import Path

def fix_migrations():
    migration_dir = Path("alembic/versions")
    print("🔧 Corrigindo imports em scripts de migração...")
    
    for file in migration_dir.glob("*.py"):
        content = file.read_text(encoding="utf-8")
        if "app.models.core" in content and "import app.models.core" not in content:
            print(f"   ✅ Corrigindo: {file.name}")
            # Insere o import logo após os imports padrão do alembic
            new_content = content.replace(
                "import sqlalchemy as sa",
                "import sqlalchemy as sa\nimport app.models.core"
            )
            file.write_text(new_content, encoding="utf-8")

if __name__ == "__main__":
    fix_migrations()

