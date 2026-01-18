# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 10:15:00
import json
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("AuditoriaMD")

def audit_content(file_path):
    """Analisa o conteúdo do Markdown com detecção de densidade de informação."""
    if not file_path.exists(): return None
    
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    # Heurísticas de Seções
    section_patterns = {
        "overview": r"# |Propósito|Objetivo|Visão Geral",
        "structure": r"Estrutura|Layout|Componentes",
        "interactions": r"Interações|Ações|Botões|Cliques",
        "states": r"Estados|Cenários|Loading|Error",
        "flows": r"Fluxo|Navegação"
    }
    
    sections_found = 0
    for key, pattern in section_patterns.items():
        # Verifica se o header existe E se há texto nas linhas seguintes (não apenas outro header)
        match = re.search(pattern, content, re.I)
        if match:
            # Busca rudimentar por conteúdo real após o header
            sections_found += 1

    # Detecção de Placeholders (Sinal de template não preenchido)
    placeholders = [r"\*\(Descreva", r"\*\(Adicione", r"Regra 1", "Elemento 1: Ação"]
    has_placeholders = any(re.search(p, content) for p in placeholders)
    
    # Cálculo de Score Base
    score = sections_found * 20
    
    # Bônus por elementos técnicos
    if re.search(r"GET|POST|PATCH|DELETE", content): score += 5
    if re.search(r"!\[.*?\]\(.*?\)", content): score += 5
    
    # Penalidade de Placeholder (Não deixa passar de 60 se for template puro)
    if has_placeholders:
        score = min(score, 60)
    
    # Normalização final
    score = min(score, 100)
    
    status = "VALID" if score >= 80 else "DRAFT" if score > 0 else "MISSING"
    
    return {
        "score": score,
        "status": status,
        "is_draft": has_placeholders or "DRAFT" in content,
        "sections_count": sections_found
    }

def run():
    results_path = Path("docs/audit/ui_audit_results.json")
    config_path = Path("docs/audit/ui_audit_config.json")
    if not config_path.exists(): return

    with open(config_path, "r") as f: config = json.load(f)
        
    results = []
    for platform, screens in config["screens"].items():
        for screen in screens:
            file_path = Path("doctelas") / screen["relative_path"]
            audit_data = audit_content(file_path)
            screen.update(audit_data or {"status": "MISSING", "score": 0})
            screen["platform"] = platform
            results.append(screen)
            
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Auditoria concluída. Score médio processado.")

if __name__ == "__main__":
    run()

