# DOMAIN: FINTECH / SAAS
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-10
TITLE: SaaS Billing Engine & Metered Usage (Stripe)
OWNER: Executor Kernel
PRIORITY: CRÍTICA (MONETIZATION)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema possui integração básica com Stripe para planos fixos.
- Não há cobrança baseada em uso (Metered Billing) ou volume de transações.
- O faturamento de comissões de vendas offline (dinheiro) é manual.
- Não existe um dashboard de "Minha Fatura" para o lojista.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação de `Stripe Usage Records` para cobrança variável.
- Automação de faturamento: Assinatura Fixa + % de Vendas Offline.
- Bloqueio automático de acesso (Soft Lock) em caso de inadimplência.
- Dashboard de transparência de cobrança no Admin.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Webhooks de fatura (invoice.created, invoice.paid).
- Lógica de sincronização de uso (Usage Reporting) diária.
- UI de extrato de cobrança.

### EXCLUI
- Negociação de taxas customizadas por cliente (usar tiers padrão).

✅ 5. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
- [ ] O sistema reporta o volume de vendas ao Stripe via API.
- [ ] O lojista consegue ver o valor acumulado da próxima fatura.
