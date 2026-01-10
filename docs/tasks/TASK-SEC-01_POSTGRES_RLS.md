# DOMAIN: BACKEND
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-SEC-01
TITLE: Implementar PostgreSQL Row-Level Security (RLS)
OWNER: Executor Kernel
PRIORITY: CRÍTICA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O isolamento multi-tenant é feito via código Python utilizando filtros manuais `.filter(company_id=...)`.
- O banco PostgreSQL (Neon) possui RLS desativado por padrão em todas as tabelas.
- Existe um risco elevado de vazamento de dados caso um desenvolvedor esqueça de aplicar o filtro em novos endpoints ou queries complexas.
- A auditoria de acesso depende de logs de aplicação que podem ser ignorados.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Todas as tabelas core (`companies`, `orders`, `products`, `tables`, `employees`, `categories`) possuem `ENABLE ROW LEVEL SECURITY`.
- Implementação de uma política global `tenant_isolation_policy` que filtra linhas baseado no valor da variável de sessão `app.current_company_id`.
- O arquivo `app/database.py` configura automaticamente o ID da empresa na sessão do banco de dados imediatamente após a validação do token JWT.
- Tentativas de acesso a dados de outro tenant resultam em zero linhas retornadas pelo banco, independentemente do código Python.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Geração de script SQL de migração para ativação de RLS e criação de políticas.
- Refatoração do `get_db` ou criação de middleware no FastAPI para executar `SET app.current_company_id`.
- Implementação de testes de segurança que tentam burlar o isolamento.
### EXCLUI
- Remoção dos filtros `.filter()` manuais existentes (serão mantidos como camada de redundância).
- Alteração de lógica de negócio nos routers.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Banco de Dados: PostgreSQL 15+.
- ORM: SQLAlchemy 2.0 (Async).
- Alterar arquitetura: SIM (Camada de Persistência).
- Criar novos serviços: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Arquivo `app/database.py`.
- Arquivo `app/models.py`.
- Acesso ao banco de dados via engine SQLAlchemy.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Script de migração SQL.
- Arquivo `app/database.py` atualizado.
- Script de validação `scripts/validation/verify_TASK-SEC-01.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] Comando `SHOW ROW LEVEL SECURITY` para tabelas core retorna `ON`.
- [ ] Uma query executada sem filtro manual retorna apenas dados do tenant logado.
- [ ] O sistema não apresenta overhead de performance superior a 5% em queries de leitura.
- [ ] Script de validação retorna Exit Code 0.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/validation/verify_TASK-SEC-01.py`
RESULTADO_ESPERADO: Confirmação de que o banco bloqueou acesso cross-tenant.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Executar `ALTER TABLE ... DISABLE ROW LEVEL SECURITY`.
- Remover políticas via `DROP POLICY`.
- Reverter alterações no `app/database.py`.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO desativar o RLS para o usuário da aplicação (apenas para o superuser de migração).
- É PROIBIDO trafegar o `company_id` em texto plano sem validação de JWT.
