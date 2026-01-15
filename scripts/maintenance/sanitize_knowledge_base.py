# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:55:00
import sys, io
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def sanitize():
    kb_file = Path("docs/technical/AI_KNOWLEDGE_BASE.md")
    if not kb_file.exists():
        print("❌ Arquivo não encontrado.")
        return

    print("🧹 Sanitizando Base de Conhecimento (Removendo poluição de código)...")
    content = kb_file.read_text(encoding="utf-8")
    
    # Mantém apenas o cabeçalho e as entradas de aprendizado reais
    # Remove blocos que contenham [[MESAFLOW_BEGIN]] (código vazado)
    lines = content.splitlines()
    new_lines = []
    skip = False
    
    for line in lines:
        if "[[MESAFLOW_BEGIN" in line:
            skip = True
            continue
        if "[[MESAFLOW_END" in line:
            skip = False
            continue
        if not skip:
            new_lines.append(line)

    kb_file.write_text("\n".join(new_lines), encoding="utf-8")
    print("✅ Memória limpa e otimizada.")

if __name__ == "__main__":
    sanitize()

