# 🔥 Protocolo de Hotfix L5.1

**Objetivo:** Correção emergencial em produção sem quebrar a governança.

## 1. Critérios de Acionamento
Um Hotfix L5.1 só é autorizado se:
- **Crash Rate** > 0.5% (Sentry Alert).
- **Bloqueio de Receita** (Falha no Checkout/Pagamento).
- **Vazamento de Dados** (Segurança).

## 2. Fluxo de Execução (Fast Track)
1.  **Branch:** Criar branch `hotfix/descrição-do-erro` a partir da `main`.
2.  **Correção:** Aplicar o fix mínimo necessário (Surgical Fix).
3.  **Validação:**
    - Rodar `scripts/run_mobile_ci.bat` (Obrigatório).
    - O UI Sweep deve passar 100%.
4.  **Deploy:**
    - Utilizar `eas update` (OTA) para correção imediata se for JS.
    - Utilizar `eas build` apenas se for nativo.

## 3. Pós-Incidente
- Atualizar `PRODUCTION_LOCK_MOBILE.json` com nova versão.
- Gerar relatório de Post-Mortem em `docs/reports/incidents/`.
- O Kernel deve reavaliar a regra que permitiu o erro.

---
**Regra de Ouro:** "Rápido, mas nunca sujo. A governança prevalece sobre a pressa."