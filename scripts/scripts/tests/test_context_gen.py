# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-08 10:35:00
import pytest
from pathlib import Path
from gerartxt import is_ignored

def test_ignore_logic_v9():
    """
    Valida a lógica de exclusão do gerartxt v9.2.
    """
    
    # 1. Casos que DEVEM ser ignorados (Ruído/Binários/Cache)
    assert is_ignored(Path("node_modules/react/index.js")) is True
    assert is_ignored(Path(".git/config")) is True
    # .pyc é ignorado pela extensão
    assert is_ignored(Path("app/main.pyc")) is True
    assert is_ignored(Path("mobile/android/build/output.apk")) is True
    assert is_ignored(Path(".env")) is True
    assert is_ignored(Path("package-lock.json")) is True
    
    # 2. Casos que DEVEM ser incluídos (Código Fonte/Docs)
    assert is_ignored(Path("app/main.py")) is False
    assert is_ignored(Path("frontend/src/index.ts")) is False
    assert is_ignored(Path("docs/README.md")) is False
    assert is_ignored(Path("scripts/setup/setup.py")) is False
