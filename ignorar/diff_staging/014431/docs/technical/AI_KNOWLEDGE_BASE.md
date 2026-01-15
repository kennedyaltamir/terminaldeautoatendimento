# 🧠 MesaFlow AI Knowledge Base (Immune System)
**Status:** APPEND-ONLY / MANDATORY
**Versão:** 4.1 (Gold Master Consolidation)

---

## 🏁 ESTADO ATUAL: GOLD MASTER SEALED (2026-01-15)
O sistema MesaFlow OS atingiu a maturidade L6. Todos os gates técnicos foram validados.

---

## 🛠️ APRENDIZADOS CRÍTICOS & PADRÕES

### 2026-01-15 | ENV_TEMPLATE_CONSOLIDATION
- **Fato:** Identificada a necessidade de incluir variáveis de SMTP e S3 no template mestre.
- **Regra:** O `.env.example` deve conter 100% das variáveis declaradas no `app/core/config.py` (ou equivalentes) para garantir o deploy "Zero-Touch".
- **Segurança:** A variável `SUPER_ADMIN_SECRET` é mandatória para operações de suporte via API.

### 2026-01-15 | KERNEL_STRICT_LEARNING (v8.3)
- **Regra:** O `atualizar.py` agora bloqueia execuções que não contenham a tag `<Knowledge_Accumulation>`.

### 2026-01-15 | FISCAL_SANDBOX_READY
- **Status:** Integração com Focus NFe validada via `smoke_test_focus_nfe.py`.
- **Bloqueio de Produção:** Exige Certificado Digital A1 (.pfx).

### 2026-01-15 | UI_PRICE_FORMATTING_FIX
- **Padrão:** Sempre utilizar a função `formatCurrency(valueInCents)` do `lib/utils.ts`.

