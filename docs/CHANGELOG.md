# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-09
# 📝 Changelog - MesaFlow

## [4.0.2] - 2026-01-09 - "Global Identity"
Fundação para a rede global de usuários.

### 🌐 MesaFlow Passport
- **Global Schema:** Implementação das tabelas `global_users` e `global_wallets` no banco de dados.
- **Interoperabilidade:** Estrutura preparada para saldo compartilhado entre tenants.

---

## [4.0.1] - 2026-01-09 - "Predictive Intelligence"
Lançamento do primeiro módulo de IA Preditiva.

### 🧠 Inteligência Artificial
- **Demand Prediction:** Novo endpoint `/api/admin/ai/forecast` que utiliza Regressão Linear (Scikit-Learn) para prever vendas futuras com base no histórico de 90 dias.
- **Data Science Stack:** Inclusão de `pandas` e `scikit-learn` no backend.

---

## [4.0.0-alpha] - 2026-01-09 - "Intelligence Era"
Início do Ciclo 4: Foco em Inteligência Artificial, Efeitos de Rede e Expansão Global.

### 🧠 Planejamento
- **Blueprint IGS:** Definição da arquitetura para Previsão de Demanda e Identidade Global (Passport).
- **Backlog:** Criação das tasks `TASK-AI-01`, `TASK-NET-01`, `TASK-UX-01` e `TASK-GLO-01`.

---

## [3.2.3] - 2026-01-09 - "Monetization Engine"
Implementação do motor de faturamento variável para SaaS.

### 💰 Fintech & SaaS
- **Metered Billing:** Integração com Stripe Usage Records para cobrança de comissões variáveis (vendas offline).
- **Reporte de Uso:** Serviço automatizado para envio de métricas de consumo ao Stripe.

### 📱 Mobile
- **OTA Updates:** Configuração completa do `expo-updates`. O aplicativo agora suporta hotfixes (correções de JS/Assets) sem necessidade de nova submissão às lojas.
- **Canais de Release:** Definição de canais `preview` e `production` no EAS para gestão de versões.

### 🚀 Growth (GTM)
- **Onboarding Zero-Touch:** Implementado importador de cardápio iFood. Novos usuários agora podem popular seu catálogo automaticamente inserindo a URL pública do iFood.
- **Auto-Setup:** Criação automática de mesa e QR Code no momento do registro.

### 🛡️ Segurança & Compliance
- **SCA (Software Composition Analysis):** Implementada auditoria automatizada de dependências (`pip-audit`, `npm audit`) no pipeline de CI/CD.
- **Vulnerability Remediation:** Correção de CVEs críticos em `aiohttp`, `requests`, `next` e outras bibliotecas core.
- **Governance Gates:** O pipeline de CI agora bloqueia deploys que não atendam aos requisitos de documentação (ADR, Risco, Compliance).

### ☁️ Infraestrutura & Ops
- **Cloud Storage:** Integração agnóstica com S3/R2 para persistência de uploads em produção (substituindo armazenamento local efêmero).
- **SMTP Real:** Serviço de e-mail transacional implementado para recuperação de senha e notificações.
- **Load Testing:** Suíte de testes de carga com **Locust** para validação de capacidade e escalabilidade.
- **Pre-Flight Checks:** Scripts de validação de conectividade para todas as integrações externas (Stripe, MP, WhatsApp, Banco).

---

## [3.1.1] - 2026-01-08 - "Hardening & Infrastructure Pivot"
Esta versão marca uma mudança estratégica: a interrupção de novas funcionalidades de UI para focar na blindagem do core Enterprise.

### 🛡️ Segurança & Infraestrutura
- **PostgreSQL RLS:** Implementação de isolamento multi-tenant nativo no banco de dados.
- **Webhooks iFood:** Substituição do polling por Webhooks de entrada (`Inbound Webhooks`) com validação HMAC.
- **Precisão Financeira:** Refatoração para Centavos (Inteiros) em todo o sistema.
- **Mobile Power Save:** Otimização do `GlobalClockService` para economia de bateria.

---

## [3.0.0] - 2026-01-05 - "The Enterprise Milestone"
Lançamento da versão Enterprise com suporte a Fiscal, Integrações e Mobile Nativo.

### ✨ Novidades
- **Contingência Fiscal:** Emissão de notas offline.
- **Hub iFood:** Integração nativa.
- **Webhooks de Saída:** Notificações para sistemas externos.
- **Motor de Promoções:** Cupons e regras de desconto.

---

## [2.3.2] - 2026-01-05 - "CI/CD Stabilization"
- Correção de regressões na suíte de testes.
- Implementação de GUID híbrido.

---

## [2.2.0] - 2026-01-03 - "Fintech & Mobile Operations"
- Split de Pagamento (Pix).
- Gestão de Assinaturas (Stripe).
- Dashboard Financeiro Real.

---

## [2.1.0] - 2026-01-02 - "Enterprise Polish"
- Menu com Navegação "Sticky".
- KDS com SLA Timer.
- WebSocket com reconexão automática.

---

## [2.0.0] - 2025-12-31 - "MVP Híbrido"
- Lançamento inicial com Cardápio Digital, KDS e Gestão de Mesas.
