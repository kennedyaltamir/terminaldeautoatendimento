# 🧠 MesaFlow AI Knowledge Base (Immune System)
**Status:** APPEND-ONLY / MANDATORY
**Versão:** 4.2 (Integrations Sync)
**Objetivo:** Memória persistente para evitar repetição de erros técnicos e garantir a soberania do Kernel.

---

## 🏁 ESTADO ATUAL: GOLD MASTER SEALED (2026-01-15)
O sistema MesaFlow OS atingiu a maturidade L6. Todos os gates técnicos foram validados.

---

## 🛠️ APRENDIZADOS CRÍTICOS & PADRÕES

### 2026-01-15 | LANDING_PAGE_INTEGRATIONS_UPDATE
- **Fato:** A seção de integrações da Landing Page foi atualizada para refletir o stack real: Stripe, Mercado Pago, FocusNFe, Sentry, Neon, Redis e Render.
- **Padrão:** Componentes de marketing devem ser atualizados sempre que um novo provedor de infraestrutura core for homologado.

### 2026-01-15 | ENV_TEMPLATE_CONSOLIDATION
- **Fato:** Identificada a necessidade de incluir variáveis de SMTP e S3 no template mestre.
- **Regra:** O `.env.example` deve conter 100% das variáveis declaradas no `app/core/config.py`.

### 2026-01-15 | KERNEL_STRICT_LEARNING (v8.3)
- **Regra:** O `atualizar.py` agora bloqueia execuções que não contenham a tag `<Knowledge_Accumulation>`.

### 2026-01-15 | FISCAL_SANDBOX_READY
- **Status:** Integração com Focus NFe validada via `smoke_test_focus_nfe.py`.

### 2026-01-15 | UI_PRICE_FORMATTING_FIX
- **Padrão:** Sempre utilizar a função `formatCurrency(valueInCents)` do `lib/utils.ts` para exibição.

