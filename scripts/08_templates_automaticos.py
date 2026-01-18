# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 09:57:00
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Templates")

TEMPLATE = """# 📱 {name}
> **Plataforma:** {platform}
> **Rota:** `{route}`
> **Status:** DRAFT (Auto-generated)

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Estrutura Técnica
**Arquivo Fonte:** `{source}`

## 3. Elementos Interativos
- [ ] Elemento 1: Ação

## 4. Regras de Negócio
- Regra 1

---
*Gerado pelo Kernel MesaFlow L6.*
"""

def run():
    results_path = Path("docs/audit/ui_audit_results.json")
    if not results_path.exists(): return

    with open(results_path, "r") as f: results = json.load(f)
    
    created = 0
    for s in results:
        if s["status"] == "MISSING":
            file_path = Path("doctelas") / s["platform"] / f"{s['normalized_name']}.md"
            if not file_path.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
                content = TEMPLATE.format(
                    name=s["normalized_name"],
                    platform=s["platform"],
                    route=s["route"],
                    source=s["file_name"]
                )
                file_path.write_text(content, encoding="utf-8")
                created += 1
                logger.info(f"   [+] Criado: {s['platform']}/{s['normalized_name']}.md")
                
    logger.info(f"Total de templates gerados: {created}")

if __name__ == "__main__":
    run()

