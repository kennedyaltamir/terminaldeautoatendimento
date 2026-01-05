import os
import pytest
import importlib.util

def test_screenshot_script_exists():
    """Verifica se o script de captura foi criado no local correto."""
    script_path = "scripts/functional/capture_screenshots.py"
    assert os.path.exists(script_path), f"Script não encontrado em {script_path}"

def test_playwright_dependency():
    """
    Verifica se o Playwright está instalado no ambiente Python.
    """
    spec = importlib.util.find_spec("playwright")
    if spec is None:
        pytest.fail("❌ Playwright não está instalado. Rode: pip install playwright && playwright install chromium")
    else:
        print("✅ Playwright detectado.")
