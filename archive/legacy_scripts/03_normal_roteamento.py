# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 10:30:00
import json
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Normalizacao")

def to_pascal_case(text):
    """Converte para PascalCase limpando sufixos de forma absoluta."""
    # 1. Remove extensão
    text = re.sub(r"\.md$", "", text, flags=re.I)
    # 2. Remove sufixos Page/Screen em qualquer variação de caixa
    text = re.sub(r"(page|screen)$", "", text, flags=re.I)
    # 3. Divide e capitaliza
    parts = re.split(r'[^a-zA-Z0-9]', text)
    return "".join([p[0].upper() + p[1:] if p else "" for p in parts])

def run():
    results_path = Path("docs/audit/ui_audit_results.json")
    if not results_path.exists(): return

    with open(results_path, "r") as f: results = json.load(f)
        
    for screen in results:
        platform = screen["platform"]
        base_name = to_pascal_case(screen["file_name"])
        
        suffix = "Page" if platform == "web" else "Screen"
        screen["normalized_name"] = base_name + suffix
        
        # Roteamento
        if platform == "web":
            route = base_name.replace("Admin", "")
            screen["route"] = f"/{route.lower()}" if "Admin" not in base_name else f"/admin/{route.lower()}"
        else:
            screen["route"] = f"Native://{base_name}"
            
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info("Nomenclatura normalizada (v2.2 - Sufixo Único Garantido).")

if __name__ == "__main__":
    run()

