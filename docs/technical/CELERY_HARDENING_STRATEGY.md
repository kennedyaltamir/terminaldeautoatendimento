# ⚙️ Celery Hardening: Backoff e Isolamento de Recursos
**Versão:** 10.0.1-AUTO | **Domínio:** BACKEND | **Status:** ACTIVE

## 1. Backoff Adaptativo (Anti-Retry Storm)
Em cenários de falha massiva do provedor (ex: Mercado Pago fora do ar):
- O sistema detecta o aumento na taxa de erro (`error_rate > 50%`).
- O `backoff_factor` é dobrado automaticamente.
- Tasks de baixa prioridade são movidas para a fila `parking_lot` para liberar workers.

## 2. Isolamento de Recursos de Banco
- **Dedicated Connection Pool:** Workers Celery utilizam um pool separado da API para evitar que uma tempestade de tasks esgote as conexões do banco.
- **Statement Timeout:** Tasks de BI/Relatórios possuem timeout de 30s; Tasks transacionais possuem timeout de 5s.

## 3. Visualização de Fluxo
O comando `python scripts/observability/trace_tasks.py` gera um diagrama Mermaid em tempo real do estado das filas e dependências ativas.

