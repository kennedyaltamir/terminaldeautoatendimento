# DOMAIN: OPERATIONS
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-OPS-01
TITLE: Production Secrets & Integration Validation (Real World Connect)
OWNER: Executor Kernel
PRIORITY: CRÍTICA (SALES ENABLEMENT)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema possui toda a lógica de integração implementada (Stripe, MP, Fiscal, WhatsApp), mas opera majoritariamente com chaves de teste, mocks ou variáveis não configuradas.
- Não existe um arquivo de referência `.env.production.template` que liste exaustivamente todas as variáveis necessárias para a operação real.
- Não há um mecanismo automatizado para validar se as credenciais de produção inseridas são válidas (Connectivity Check) antes do deploy.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Criação de um template de ambiente de produção (`.env.production.template`) documentado.
- Implementação de um script de "Pre-Flight Check" (`scripts/production/validate_integrations.py`) que testa a conectividade real com Stripe, Mercado Pago, Neon e Evolution API usando as chaves fornecidas.
- O sistema sai do estado "Mock" para "Connected", pronto para transacionar dinheiro real.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Mapeamento de todas as variáveis de ambiente críticas.
- Script de geração de template `.env`.
- Script de validação de conectividade (Ping em APIs externas).
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Geração das chaves em si (o usuário deve obter nos portais).
- Execução de transações financeiras reais (apenas validação de credenciais).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Segurança: O script de validação NÃO deve exibir as chaves no terminal, apenas o status (OK/ERRO).
- Dependências: `requests`, `stripe`, `psycopg2`.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Lista de serviços externos utilizados.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `.env.production.template`
- `scripts/setup/generate_prod_env.py`
- `scripts/production/validate_integrations.py`

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Template de env cobre Banco, Redis, Stripe, MP, Fiscal, Auth e Logs.
- [x] Script de validação testa conexão com Banco de Dados.
- [x] Script de validação testa autenticação com Stripe (se chave presente).
- [x] Script de validação testa autenticação com Mercado Pago (se chave presente).

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/validate_integrations.py`
RESULTADO_ESPERADO: "Integration Check: All configured services are reachable."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover scripts criados.
