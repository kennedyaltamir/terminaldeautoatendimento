# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-08 19:15:00
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-01
TITLE: Infraestrutura Blindada (Neon Pooled + Render)
OWNER: Executor Kernel
PRIORITY: CRÍTICA (GTM)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema roda em ambiente de desenvolvimento ou produção simulada.
- A conexão com o banco de dados não utiliza pooling explícito (PgBouncer) na string de conexão, o que pode causar "Connection Limit Exceeded" em escala.
- O `render.yaml` existe mas pode não estar otimizado para o plano Starter.
- Não há validação automatizada de que o ambiente é "Production Grade".

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O backend utiliza obrigatoriamente a string de conexão com `-pooler` do Neon em produção.
- O `app/database.py` implementa `pool_pre_ping=True` e `pool_size` otimizado.
- O `render.yaml` define explicitamente as variáveis de ambiente críticas para performance.
- Um script de verificação confirma se a conexão é resiliente a quedas.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Ajuste fino em `app/database.py` para SQLAlchemy Engine.
- Atualização de `render.yaml` com configurações de Gunicorn Workers.
- Criação de script `scripts/production/verify_db_pool.py`.

### EXCLUI
- Contratação do serviço (deve ser feita manualmente no painel).
- Migração de dados (assumimos banco novo ou migrado via dump).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Banco: PostgreSQL (Neon.tech).
- Driver: `psycopg2-binary` ou `asyncpg`.
- Alterar arquitetura: NÃO (Apenas configuração).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/database.py`
- `render.yaml`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/database.py` otimizado.
- `render.yaml` atualizado.
- `scripts/production/verify_db_pool.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] O Engine do SQLAlchemy está configurado com `pool_size=20` e `max_overflow=10`.
- [x] O script de verificação conecta e executa 100 queries simultâneas sem erro.
- [x] O `render.yaml` especifica `WEB_CONCURRENCY` ou workers do Gunicorn.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_db_pool.py`
RESULTADO_ESPERADO: "Pool Stress Test Passed: 100/100 connections OK."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `app/database.py` para configuração padrão.