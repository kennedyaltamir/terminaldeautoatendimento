# 📝 Especificação Técnica: TASK-ENV-01
> **Título:** Auditoria e Definição de Variáveis de Ambiente
> **Status:** APROVADO
> **Objetivo:** Garantir que o sistema possua todas as chaves necessárias para operação Enterprise.

## 1. Escopo de Variáveis
As variáveis devem ser categorizadas para facilitar a manutenção:
- **CORE:** Banco de dados, Redis, Segurança JWT.
- **AUTH:** Google OAuth, Super Admin Secret.
- **FINTECH:** Stripe (Assinaturas), Mercado Pago (Split).
- **LOGISTICS:** iFood API, Webhooks.
- **INFRA:** AWS S3/R2 (Storage), SMTP (E-mail).
- **OBSERVABILITY:** Sentry (Back/Front).

## 2. Regras de Validação
- Nenhuma variável crítica pode estar vazia em produção.
- Variáveis de URL devem começar com `http://`, `https://`, `ws://` ou `wss://`.
- O arquivo `.env.example` deve conter descrições claras e valores de exemplo não sensíveis.