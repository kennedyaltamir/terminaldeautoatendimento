# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:15:00
import os
from pathlib import Path

def validate():
    print("🔍 Validando TASK-DOC-01")
    
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("❌ ERRO: README.md não encontrado na raiz.")
        exit(1)
        
    content = readme_path.read_text(encoding="utf-8")
    
    required_keywords = [
        "MesaFlow OS",
        "Tech Stack",
        "FastAPI",
        "Next.js",
        "Expo",
        "Como Iniciar"
    ]
    
    missing = []
    for kw in required_keywords:
        if kw not in content:
            missing.append(kw)
            
    if missing:
        print(f"❌ ERRO: README.md incompleto. Faltam as palavras-chave: {', '.join(missing)}")
        exit(1)
        
    print("✅ README.md validado com sucesso.")
    exit(0)

if __name__ == "__main__":
    validate()
