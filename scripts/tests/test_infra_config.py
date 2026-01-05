import os
import json
import yaml
import pytest

def test_render_yaml_exists_and_valid():
    """Verifica se o render.yaml existe e é um YAML válido."""
    assert os.path.exists("render.yaml"), "render.yaml não encontrado"
    with open("render.yaml", "r") as f:
        data = yaml.safe_load(f)
        assert "services" in data
        api_service = next((s for s in data["services"] if s["name"] == "mesaflow-api"), None)
        assert api_service is not None
        assert "gunicorn" in api_service["startCommand"]

def test_vercel_json_exists_and_valid():
    """Verifica se o vercel.json existe e é um JSON válido."""
    assert os.path.exists("vercel.json"), "vercel.json não encontrado"
    with open("vercel.json", "r") as f:
        data = json.load(f)
        assert data["framework"] == "nextjs"
        assert "rewrites" in data

def test_deploy_docs_updated():
    """Verifica se o guia de deploy menciona Neon e Render."""
    assert os.path.exists("docs/DEPLOY.md")
    with open("docs/DEPLOY.md", "r", encoding="utf-8") as f:
        content = f.read()
        assert "Neon.tech" in content
        assert "Render.com" in content
