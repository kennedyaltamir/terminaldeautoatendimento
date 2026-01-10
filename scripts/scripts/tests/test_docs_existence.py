import os
import pytest
from pathlib import Path

def test_critical_documentation_exists():
    """
    Verifica se a documentação técnica essencial para o Handover foi criada.
    Isso garante que a próxima IA não ficará 'cega'.
    """
    base_dir = Path("docs/technical")
    
    required_files = [
        "ENV_REFERENCE.md",
        "PROJECT_STRUCTURE.md",
        "DATABASE_RELATIONSHIPS.md",
        "TROUBLESHOOTING.md"
    ]
    
    print("\n🔍 Auditando Documentação Técnica...")
    
    for filename in required_files:
        file_path = base_dir / filename
        
        # 1. Verifica existência
        assert file_path.exists(), f"❌ Documento faltando: {filename}"
        
        # 2. Verifica conteúdo (não pode estar vazio)
        content = file_path.read_text(encoding="utf-8")
        assert len(content) > 50, f"⚠️ Documento vazio ou muito curto: {filename}"
        
        print(f"✅ {filename} - OK ({len(content)} bytes)")

def test_handover_prompt_exists():
    """Verifica se o prompt mestre de handover está presente."""
    prompt_path = Path("docs/Prompts/Master_Handover.xml")
    assert prompt_path.exists()
    assert "MesaFlow" in prompt_path.read_text(encoding="utf-8")
    print("✅ Master_Handover.xml - OK")
