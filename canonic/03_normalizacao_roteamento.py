# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 11:30:00
import json
import re
import logging
from pathlib import Path

"""
Script 3: normalizacao_roteamento.py (v1.1 - Robust)
Objetivo: Garantir consistência de nomes, rotas e criticidade.
Melhorias: Fallbacks para chaves ausentes e normalização de caminhos.
"""

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Step3_Normalizacao")

RESULTS_FILE = Path("docs/audit/ui_audit_results.json")
CONFIG_FILE = Path("docs/audit/ui_audit_config.json")

def infer_name(route: str, platform: str) -> str:
    if not route or route == "N/A":
        return "Unknown" + ("Page" if platform == 'web' else "Screen")
        
    clean = route.replace('\\', '/').replace('frontend/src/app', '').replace('mobile/src/screens', '').replace('/page.tsx', '').replace('.tsx', '')
    parts = [p for p in clean.split('/') if p and not (p.startswith('[') or p == "hamburgueria-ze")]
    
    if not parts: return "LandingPage" if platform == 'web' else "MainScreen"
    
    name = "".join([re.sub(r'[\W_]+', '', p).capitalize() for p in parts])
    suffix = "Page" if platform == 'web' else "Screen"
    if not name.lower().endswith(suffix.lower()): name += suffix
    return name

def run():
    if not RESULTS_FILE.exists(): 
        logger.error("Arquivo de resultados não encontrado. Execute o Step 02.")
        return
    
    results = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    
    # Fallbacks de Configuração
    norm_map = config.get("normalization_map", {})
    crit_patterns = config.get("critical_patterns", ["Login", "Dashboard", "Checkout", "Payment"])

    for screen in results:
        # 1. Garantir chaves básicas para evitar KeyError nos steps seguintes
        screen["platform"] = screen.get("platform", "unknown")
        screen["route"] = screen.get("rota") or screen.get("route") or "N/A"
        
        # 2. Normalização de Nome
        inferred = infer_name(screen["route"], screen["platform"])
        screen["name"] = norm_map.get(inferred, inferred)
        
        # 3. Identificação de Criticidade
        screen["is_critical"] = any(p.lower() in screen["name"].lower() for p in crit_patterns)

    RESULTS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"Sucesso: {len(results)} telas normalizadas e classificadas.")

if __name__ == "__main__":
    run()

