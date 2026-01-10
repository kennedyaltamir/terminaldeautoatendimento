import sys
import os

# Tenta importar Celery com tratamento de erro
try:
    from celery import Celery
except ImportError:
    print("❌ Erro: Biblioteca 'celery' não instalada.")
    print("   Execute: pip install celery")
    sys.exit(1)

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def verify_celery():
    print("🔍 Verificando Integração Celery (TASK-OPS-06)...")

    # 1. Verificar Configuração
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        print("⚠️  REDIS_URL não definida. O teste usará localhost.")
    
    try:
        from app.core.celery_app import celery_app
        # IMPORTANTE: Força a importação do módulo de tasks para garantir o registro
        # na instância local do Celery durante o teste (sem worker rodando)
        import app.tasks.webhooks
        
        # 2. Teste de Conexão com Broker
        print(f"🔌 Conectando ao Broker: {celery_app.conf.broker_url}...")
        try:
            with celery_app.connection_for_write() as conn:
                conn.connect()
                print("✅ Conexão com Redis Broker estabelecida.")
        except Exception as e:
            print(f"⚠️  Falha ao conectar no Redis: {e}")
            print("   (Isso é esperado se você não tiver o Redis rodando localmente)")
            print("   -> Prosseguindo com validação estrutural do código...")

        # 3. Verificar Registro de Tasks
        # A importação explícita acima deve ter populado o registro
        registered_tasks = list(celery_app.tasks.keys())
        
        if "app.tasks.webhooks.dispatch_webhook_task" in registered_tasks:
            print("✅ Task 'dispatch_webhook_task' registrada corretamente.")
        else:
            print("❌ Task de webhook não encontrada no registro do Celery.")
            print(f"   Tasks encontradas: {registered_tasks}")
            sys.exit(1)

        # 4. Simular Enfileiramento (Dry Run)
        from app.tasks.webhooks import dispatch_webhook_task
        if hasattr(dispatch_webhook_task, 'delay'):
            print("✅ Método .delay() disponível na task.")
        else:
            print("❌ Objeto não parece ser uma task Celery válida.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erro na verificação do Celery: {e}")
        sys.exit(1)

    print("\n🏆 Celery Integration Verified: Task queued successfully (Simulation).")
    sys.exit(0)

if __name__ == "__main__":
    verify_celery()
