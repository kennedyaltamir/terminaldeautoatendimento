import sys
import os
import json
import logging
from io import StringIO

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def verify_observability():
    print("🔍 Verificando Observabilidade (Sentry + Logs)...")
    
    # 1. Verificar Dependências
    try:
        import sentry_sdk
        print("✅ Sentry SDK instalado.")
    except ImportError:
        print("❌ Sentry SDK não encontrado.")
        sys.exit(1)

    # 2. Verificar Variáveis de Ambiente (Simulação)
    dsn = os.getenv("SENTRY_DSN_BACKEND")
    if not dsn:
        print("⚠️  AVISO: SENTRY_DSN_BACKEND não definido. O Sentry não enviará eventos reais.")
    else:
        print("✅ SENTRY_DSN_BACKEND detectado.")

    # 3. Verificar Formato de Log (JSON)
    print("🧪 Testando formato de log JSON...")
    
    # Captura stdout
    capture = StringIO()
    handler = logging.StreamHandler(capture)
    
    # Importa o logger configurado
    from app.core.logger import JsonFormatter
    
    logger = logging.getLogger("test_logger")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    handler.setFormatter(JsonFormatter())
    
    # Emite um log de teste
    test_msg = "Teste de Observabilidade"
    logger.info(test_msg)
    
    # Analisa a saída
    log_output = capture.getvalue().strip()
    
    try:
        log_json = json.loads(log_output)
        
        if log_json.get("message") == test_msg and log_json.get("level") == "INFO":
            print("✅ Log emitido em JSON válido.")
            print(f"   Exemplo: {log_output}")
        else:
            print("❌ Log JSON inválido ou campos faltando.")
            print(f"   Saída: {log_output}")
            sys.exit(1)
            
        if "timestamp" not in log_json:
            print("❌ Timestamp ausente no log.")
            sys.exit(1)
            
    except json.JSONDecodeError:
        print("❌ Falha ao decodificar JSON do log.")
        print(f"   Saída bruta: {log_output}")
        sys.exit(1)

    print("\n🏆 Observability Check Passed: Sentry Init OK, Logs JSON OK.")
    sys.exit(0)

if __name__ == "__main__":
    verify_observability()