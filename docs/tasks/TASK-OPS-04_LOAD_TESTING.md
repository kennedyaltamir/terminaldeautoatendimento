# DOMAIN: OPERATIONS
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-OPS-04
TITLE: Automated Load Testing & Capacity Planning (Locust)
OWNER: Executor Kernel
PRIORITY: ALTA (ENTERPRISE)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- A infraestrutura foi blindada (Neon Pooled, Gunicorn), mas não foi estressada em cenário realista.
- Não existem métricas concretas de "RPS Máximo" (Requests per Second) ou "Usuários Simultâneos" para apresentar a clientes Enterprise.
- O script `verify_db_pool.py` testa apenas o banco, não a aplicação completa (API + Auth + Cache).

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação de suíte de teste de carga com **Locust**.
- Simulação de cenários reais: Login -> Navegar Cardápio -> Adicionar ao Carrinho -> Checkout.
- Documento de Planejamento de Capacidade (`CAPACITY_PLANNING.md`) definindo os limites teóricos da infraestrutura atual.
- Script de execução automatizada para validação de performance pré-deploy.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Adição de `locust` em `requirements.txt`.
- Criação de `scripts/performance/locustfile.py` (Cenários de Teste).
- Criação de `docs/performance/CAPACITY_PLANNING.md`.
- Script wrapper `scripts/production/run_load_test.py`.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Execução distribuída (Cluster de Locust).
- Otimização de código (o objetivo é medir, não corrigir agora).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Ferramenta: Locust (Python).
- Métricas: Latência (p95, p99), RPS, Taxa de Erro.
- Alvo: Ambiente de Staging/Produção (via URL configurável).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Endpoints da API (`/auth/token`, `/menu`, `/orders`).

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `requirements.txt` (Atualizado).
- `scripts/performance/locustfile.py`.
- `docs/performance/CAPACITY_PLANNING.md`.
- `scripts/production/run_load_test.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] O script simula um fluxo de usuário completo (não apenas ping).
- [x] O teste suporta autenticação (pega token JWT).
- [x] O documento de capacidade define os thresholds de alerta.
- [x] O wrapper executa o teste por 10 segundos e reporta sucesso/falha baseado em erros.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/run_load_test.py`
RESULTADO_ESPERADO: "Load Test Finished: OK" (com estatísticas básicas).

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover pasta `scripts/performance`.
- Remover `locust` de `requirements.txt`.
