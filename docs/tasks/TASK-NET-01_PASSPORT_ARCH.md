# DOMAIN: BACKEND
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-NET-01
TITLE: Arquitetura MesaFlow Passport (Global ID)
OWNER: Executor Kernel
PRIORITY: CRÍTICA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema opera em silos (Multi-tenant estrito).
- Um cliente que frequenta o "Restaurante A" e o "Restaurante B" possui dois cadastros isolados (ou nenhum, se for anônimo).
- Não existe uma tabela central de usuários finais (`GlobalUser`) que atravesse os tenants.
- O saldo de cashback (`CustomerWallet`) é preso ao `company_id`.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Criação das tabelas `global_users` e `global_wallets` no banco de dados.
- O `global_users` utiliza o número de telefone (E.164) como chave única universal.
- O `global_wallets` permite que o saldo seja acumulado e gasto em qualquer parceiro da rede (preparação para interoperabilidade).
- A estrutura de dados suporta o conceito de "Passport": uma identidade única para o consumidor final.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Atualização de `app/models.py` com as novas tabelas.
- Relacionamento entre `GlobalUser` e `CustomerWallet` (migração gradual).
- Script de validação de schema.

### EXCLUI
- API de Login Global (Auth0/Firebase) nesta fase.
- Interface de usuário (App do Cliente).
- Migração de dados legados (CustomerWallet existente).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Banco: PostgreSQL.
- Integridade: `phone` deve ser único globalmente.
- Segurança: `GlobalUser` não deve ter senha nesta fase (autenticação futura via OTP).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/models.py`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/models.py` atualizado.
- `scripts/validation/verify_TASK-NET-01.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] Tabela `global_users` criada com índice único em `phone`.
- [ ] Tabela `global_wallets` criada com FK para `global_users`.
- [ ] Script de validação consegue inserir um usuário global e recuperar.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/validation/verify_TASK-NET-01.py`
