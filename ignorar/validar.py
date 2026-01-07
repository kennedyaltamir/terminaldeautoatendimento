import re
import os
import sys
from pathlib import Path

# Tentativa de importar Rich para feedback visual
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

INPUT_FILE = "resposta.txt"

# Padrões Proibidos (Placeholders de preguiça)
FORBIDDEN = [
    r"\.\.\.", 
    r"restante do código", 
    r"code omitted", 
    r"// \.\.\.", 
    r"# \.\.\."
]

def validate_protocol():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ {INPUT_FILE} não encontrado.")
        return False

    content = Path(INPUT_FILE).read_text(encoding="utf-8")
    errors = []

    # 1. Verificar Tags de Início/Fim
    begins = re.findall(r"\[\[MESAFLOW_BEGIN:(.*?)\]\]", content)
    ends = re.findall(r"\[\[MESAFLOW_END\]\]", content)
    if len(begins) != len(ends):
        errors.append(f"Divergência de tags: {len(begins)} BEGIN vs {len(ends)} END.")

    # 2. Verificar Classificação de Task
    if not re.search(r"(TRIVIAL|COMPLEXA)", content.upper()):
        errors.append("Classificação de Task (TRIVIAL/COMPLEXA) não encontrada.")

    # 3. Verificar Placeholders Proibidos (Ignorando spread operator)
    clean_content = re.sub(r"\.\.\.[a-zA-Z0-9_]+", "", content)
    for p in FORBIDDEN:
        if re.search(p, clean_content, re.IGNORECASE):
            errors.append(f"Placeholder proibido detectado: '{p}'")

    # 4. Verificar Ritual de Testes
    has_test_file = any("tests/" in b for b in begins)
    has_exemption = "[TEST_EXEMPT:" in content.upper()
    
    if not has_test_file and not has_exemption:
        errors.append("Task sem arquivo de teste e sem justificativa [TEST_EXEMPT].")

    # --- RESULTADO ---
    if errors:
        if HAS_RICH:
            console.print(Panel.fit("\n".join([f"❌ {e}" for e in errors]), title="Falha na Validação de Protocolo", style="bold red"))
        else:
            print("\n".join([f"❌ {e}" for e in errors]))
        return False
    
    if HAS_RICH:
        console.print(Panel.fit("✅ Protocolo v4.3 respeitado. Pronto para atualizar.", title="Sucesso", style="bold green"))
    else:
        print("✅ Protocolo validado.")
    return True

if __name__ == "__main__":
    if not validate_protocol():
        sys.exit(1)