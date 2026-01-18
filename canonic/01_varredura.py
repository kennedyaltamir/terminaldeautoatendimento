# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 09:50:00
import os
import json
import logging
from pathlib import Path

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Varredura")

def run():
    """Varrer doctelas/ e gerar ui_audit_config.json."""
    logger.info("Iniciando Varredura de Documentação...")
    
    base_path = Path("doctelas")
    audit_dir = Path("docs/audit")
    audit_dir.mkdir(parents=True, exist_ok=True)
    
    config = {
        "platforms": ["web", "mobile"],
        "critical_patterns": ["Dashboard", "Checkout", "Payment", "Login", "Kitchen", "Waiter", "Driver"],
        "screens": {"web": [], "mobile": []}
    }
    
    ignored = {"README.md", ".gitignore", ".DS_Store", "_archive"}
    
    for platform in config["platforms"]:
        platform_path = base_path / platform
        if not platform_path.exists():
            logger.warning(f"Pasta não encontrada: {platform_path}")
            continue
            
        for file in platform_path.rglob("*.md"):
            if file.name in ignored or "_archive" in str(file):
                continue
                
            # Identifica criticidade
            is_critical = any(p.lower() in file.name.lower() for p in config["critical_patterns"])
            
            config["screens"][platform].append({
                "file_name": file.name,
                "relative_path": str(file.relative_to(base_path)),
                "is_critical": is_critical,
                "last_modified": os.path.getmtime(file)
            })
            
    output_path = audit_dir / "ui_audit_config.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        
    logger.info(f"Inventário concluído. {len(config['screens']['web']) + len(config['screens']['mobile'])} arquivos mapeados.")
    logger.info(f"Configuração salva em: {output_path}")

if __name__ == "__main__":
    run()

