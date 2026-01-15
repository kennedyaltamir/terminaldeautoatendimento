# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:55:00
import sys
import io
import os
from pathlib import Path

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify():
    kb_file = Path("docs/technical/AI_KNOWLEDGE_BASE.md")
    
    print("🔍 Verificando Memória Imunológica...")
    
    if not kb_file.exists():
        print("❌ FALHA: Arquivo AI_KNOWLEDGE_BASE.md não encontrado.")
        return 1
        
    content = kb_file.read_text(encoding="utf-8")
    if "ENTRY:" in content:
        print(f"✅ SUCESSO: Base de conhecimento detectada ({len(content)} bytes).")
        # Mostra a última entrada
        last_entry = content.split("--- ENTRY:")[-1]
        print(f"📝 Último aprendizado registrado:\n{'-'*30}\n{last_entry.strip()}\n{'-'*30}")
        return 0
    else:
        print("⚠️  AVISO: Arquivo existe, mas está vazio ou sem entradas formatadas.")
        return 1

if __name__ == "__main__":
    sys.exit(verify())

