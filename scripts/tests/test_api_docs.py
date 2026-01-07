from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_openapi_schema_exists():
    """Verifica se o JSON do OpenAPI é gerado corretamente."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    # Sincronizado com app/main.py v3.1.0
    assert schema["info"]["title"] == "MesaFlow Enterprise API"
    assert schema["info"]["version"] == "3.1.0"

def test_docs_page_exists():
    """Verifica se a página do Swagger UI carrega."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui" in response.text

def test_tags_metadata():
    """Verifica se as tags personalizadas estão presentes no schema."""
    response = client.get("/openapi.json")
    schema = response.json()
    tags = [t["name"] for t in schema["tags"]]

    expected_tags = ["Public", "Authentication", "Admin Orders", "Admin Menu"]
    for tag in expected_tags:
        assert tag in tags, f"Tag {tag} não encontrada na documentação"
