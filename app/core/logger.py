# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-08 19:20:00
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict

class JsonFormatter(logging.Formatter):
    """
    Formatador de logs para saída JSON estruturada.
    Ideal para ingestão em ferramentas como Datadog, CloudWatch, etc.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "path": record.pathname,
        }

        # Adiciona campos extras se existirem (ex: company_id)
        if hasattr(record, "company_id"):
            log_record["company_id"] = record.company_id
        
        if hasattr(record, "user_id"):
            log_record["user_id"] = record.user_id

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)

def setup_logger(name: str = "mesaflow") -> logging.Logger:
    logger = logging.getLogger(name)
    
    # Evita duplicidade de handlers se chamado múltiplas vezes
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = JsonFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Define nível baseado em ambiente (pode ser ajustado via ENV)
        logger.setLevel(logging.INFO)
        
        # Silencia loggers muito verbosos de terceiros
        logging.getLogger("uvicorn.access").handlers = []
        logging.getLogger("uvicorn.error").handlers = []
        
    return logger

# Instância global
logger = setup_logger()