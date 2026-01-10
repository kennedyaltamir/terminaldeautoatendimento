# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-08 19:15:00
import sys
import os
import time
import threading
from sqlalchemy import text, create_engine
from sqlalchemy.exc import OperationalError

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SQLALCHEMY_DATABASE_URL

# Configuração do Teste de Stress
CONCURRENT_THREADS = 50
TOTAL_REQUESTS = 100

def stress_worker(engine, results, index):
    """Worker que tenta obter uma conexão e executar uma query simples."""
    try:
        start_time = time.time()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        duration = (time.time() - start_time) * 1000
        results.append({"status": "OK", "duration": duration})
        # print(f"✅ Thread {index}: Conexão OK ({duration:.2f}ms)")
    except Exception as e:
        results.append({"status": "ERROR", "error": str(e)})
        print(f"❌ Thread {index}: Falha - {e}")

def verify_pool():
    print(f"🚀 Iniciando Teste de Stress do Pool de Conexões...")
    print(f"   URL Alvo: {SQLALCHEMY_DATABASE_URL.split('@')[1] if '@' in SQLALCHEMY_DATABASE_URL else 'Local/SQLite'}")
    print(f"   Threads Simultâneas: {CONCURRENT_THREADS}")

    # Recria a engine localmente para garantir isolamento do teste
    # Usa as mesmas configs do app/database.py
    pool_config = {
        "pool_size": 20,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_pre_ping": True
    }
    
    if "sqlite" in SQLALCHEMY_DATABASE_URL:
        print("⚠️  Aviso: Testando em SQLite. O pooling não é representativo de produção.")
        connect_args = {"check_same_thread": False}
        engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
    else:
        engine = create_engine(SQLALCHEMY_DATABASE_URL, **pool_config)

    threads = []
    results = []

    start_global = time.time()

    # Dispara threads
    for i in range(TOTAL_REQUESTS):
        t = threading.Thread(target=stress_worker, args=(engine, results, i))
        threads.append(t)
        t.start()
        
        # Limita a concorrência real para não matar a máquina local de teste
        if len(threads) >= CONCURRENT_THREADS:
            for t in threads:
                t.join()
            threads = []

    # Aguarda restantes
    for t in threads:
        t.join()

    end_global = time.time()
    total_time = end_global - start_global

    # Análise
    success_count = sum(1 for r in results if r["status"] == "OK")
    error_count = sum(1 for r in results if r["status"] == "ERROR")
    avg_latency = sum(r["duration"] for r in results if r["status"] == "OK") / success_count if success_count > 0 else 0

    print("\n📊 Relatório de Performance do Pool:")
    print(f"   Total de Requisições: {TOTAL_REQUESTS}")
    print(f"   Sucessos: {success_count}")
    print(f"   Erros: {error_count}")
    print(f"   Latência Média: {avg_latency:.2f}ms")
    print(f"   Tempo Total: {total_time:.2f}s")

    if error_count == 0:
        print("\n✅ Pool Stress Test Passed: 100/100 connections OK.")
        sys.exit(0)
    else:
        print("\n❌ Pool Stress Test Failed.")
        sys.exit(1)

if __name__ == "__main__":
    verify_pool()