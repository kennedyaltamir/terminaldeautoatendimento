# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-08 23:55:00
import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Configuração do Broker
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "mesaflow_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.webhooks"] # Registra os módulos de tasks
)

# Configurações de Produção
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Resiliência
    task_acks_late=True, # Só confirma se terminar sem erro
    task_reject_on_worker_lost=True, # Re-enfileira se o worker morrer
    broker_connection_retry_on_startup=True,
)

if __name__ == "__main__":
    celery_app.start()
