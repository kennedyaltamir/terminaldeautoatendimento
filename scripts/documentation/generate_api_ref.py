# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 19:30:00
import json
import sys
import os
from pathlib import Path

# Adiciona raiz ao path
sys.path.append(os.getcwd())

# Tenta importar o app para extrair o OpenAPI
try:
    from app.main import app
    from fastapi.openapi.utils import get_openapi
except ImportError:
    print("❌ Erro: Não foi possível importar a aplicação FastAPI.")
    sys.exit(1)

OUTPUT_FILE = Path("docs/API.md")

def generate_markdown():
    print("🔄 Gerando Referência de API (OpenAPI -> Markdown)...")
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )

    md_lines = []
    md_lines.append(f"# 🔌 {openapi_schema['info']['title']} v{openapi_schema['info']['version']}")
    md_lines.append(f"> **Gerado Automaticamente em:** {os.times()}")
    md_lines.append("\n" + openapi_schema['info']['description'] + "\n")

    for path, methods in openapi_schema['paths'].items():
        for method, details in methods.items():
            summary = details.get('summary', 'Sem descrição')
            tags = ", ".join(details.get('tags', []))
            
            md_lines.append(f"## {method.upper()} `{path}`")
            md_lines.append(f"**Resumo:** {summary}")
            if tags:
                md_lines.append(f"**Tags:** {tags}")
            
            # Parâmetros
            if 'parameters' in details:
                md_lines.append("\n### Parâmetros")
                md_lines.append("| Nome | Local | Obrigatório | Tipo |")
                md_lines.append("| :--- | :--- | :---: | :--- |")
                for param in details['parameters']:
                    required = "✅" if param.get('required') else "❌"
                    p_type = param.get('schema', {}).get('type', 'any')
                    md_lines.append(f"| `{param['name']}` | {param['in']} | {required} | {p_type} |")
            
            md_lines.append("\n---\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"✅ Documentação de API atualizada em: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_markdown()

