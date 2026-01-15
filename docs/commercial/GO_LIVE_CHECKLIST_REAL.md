
# 🚀 Checklist de Go-Live (Produção Real)
**Data Alvo:** Imediata
**Status:** PRE-FLIGHT

---

## 1. Infraestrutura & Ambiente
- [ ] **Variáveis de Ambiente (.env):**
    - [ ] `ENVIRONMENT=production`
    - [ ] `DEBUG=False`
    - [ ] `SENTRY_DSN_BACKEND` configurado (BLOQUEANTE ATUAL).
    - [ ] `SECRET_KEY` rotacionada e forte.
- [ ] **Banco de Dados:**
    - [ ] Migrations aplicadas (`alembic upgrade head`).
    - [ ] RLS ativado e validado (`verify_TASK-SEC-01.py`).
    - [ ] Backup inicial (Snapshot) realizado.

## 2. Segurança
- [ ] **HTTPS:** Forçado em todas as rotas.
- [ ] **CORS:** Restrito aos domínios de produção (`app.mesaflow.com`, etc).
- [ ] **Admin:** Senha do Super Admin alterada e forte.

## 3. Integrações
- [ ] **Pagamentos:** Chaves de Produção (Live Keys) do Stripe e Mercado Pago configuradas.
- [ ] **Webhooks:** URLs de callback configuradas nos painéis dos fornecedores.
- [ ] **WhatsApp:** Instância de produção conectada.

## 4. Mobile
- [ ] **Build:** Versão Release (AAB/IPA) gerada.
- [ ] **Assinatura:** Keystores e Certificados seguros.
- [ ] **API URL:** Apontando para `https://api.mesaflow.com` (não localhost).

## 5. Plano de Contingência
- [ ] **Rollback:** Script de reversão de deploy testado.
- [ ] **Status Page:** Página de status pública configurada.
- [ ] **Suporte:** Canal de atendimento de emergência definido.

---

**Assinatura do Responsável:** _________________________________________________
*(Só assine se OBS-01 estiver verde)*

