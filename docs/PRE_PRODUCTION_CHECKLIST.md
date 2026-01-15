# 🚀 Checklist de Pré-Produção (Hard Gate L6)

Este documento define as condições **obrigatórias** para que o sistema seja movido para o ambiente de produção real. Ignorar qualquer item resultará em veto imediato.

## 1. Segurança (Cybersecurity)
- [ ] **RLS Ativo:** Nenhuma tabela transacional pode ser lida sem `app.current_company_id`.
- [ ] **Secrets Audit:** `.env` de produção não contém chaves de teste ou locais.
- [ ] **JWT Hardening:** Refresh tokens com expiração curta e rotação ativa.
- [ ] **Boundary Audit:** Todos os headers de segurança (HSTS, CSP) ativos no `main.py`.

## 2. Infraestrutura (Reliability)
- [ ] **Healthcheck:** Todos os serviços (DB, Redis, API) reportando `UP` em `/health`.
- [ ] **Latency Check:** Latência média da API abaixo de 300ms em condições normais.
- [ ] **Backup Plan:** PITR (Point-in-Time Recovery) configurado no Neon.

## 3. Aplicação (Logic)
- [ ] **Omni-Check PASS:** O script de regressão total retornou `SUCCESS`.
- [ ] **Ledger Integrity:** A cadeia de hashes financeira está válida e sem órfãos.
- [ ] **Mobile Lock:** `PRODUCTION_LOCK_MOBILE.json` gerado e assinado.

## 📖 Explicação do Checklist
Este checklist não é sugestivo, ele é **discretivo**. 
- O RLS é o coração da nossa confiança multi-tenant. 
- O Omni-Check é o escudo contra o retrabalho que você está enfrentando. 
- A Observabilidade (Sentry) garante que se algo quebrar, seremos os primeiros a saber, não o cliente.

