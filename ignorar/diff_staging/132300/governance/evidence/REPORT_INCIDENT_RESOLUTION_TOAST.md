# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 13:30:00
# 🛡️ Relatório de Resolução de Incidente: Toast Race Condition
**ID:** INC-UI-20260115-001
**Status:** ✅ RESOLVIDO
**Severidade:** ALTA (Flakiness em Testes Críticos)

## 1. Diagnóstico Final
A falha intermitente nos testes E2E foi identificada como uma **Condição de Corrida Temporal** entre o ciclo de vida do componente de página e a duração da notificação (Toast).

### Causa Raiz
1.  **Acoplamento Indevido:** O componente `<Toaster />` residia dentro de `DriverPage`.
2.  **Desmontagem Prematura:** Ao finalizar a entrega, a lógica `setActiveDeliveryId(null)` causava o unmount da página, destruindo o Toaster antes que a animação de saída ou a asserção do teste pudessem ocorrer.
3.  **Deadlock de Teste:** O Playwright aguardava sequencialmente o desaparecimento do painel (lento) antes de verificar o Toast (rápido), perdendo a janela de observação.

## 2. Solução Aplicada (Arquitetura L6)
### A. Elevação de Estado (Hoisting)
O `<Toaster />` foi movido para `AdminLayout`, tornando-se um **Singleton de UI** persistente. Isso garante que notificações sobrevivam a navegações e desmontagens de rotas filhas.

### B. Paralelismo em Testes
Implementado `Promise.all` no Playwright para verificar condições de sucesso (Toast visível) e limpeza de estado (Painel invisível) simultaneamente, eliminando a dependência temporal.

## 3. Validação Técnica
- **Arquitetura:** Aprovada (Desacoplamento UI/Page).
- **Testes:** Aprovados (Estratégia robusta de concorrência).
- **Código:** Aprovado (Limpeza de `DriverPage`).

## 4. Lições Aprendidas (Knowledge Base)
> "Toasts e Notificações Globais nunca devem depender do ciclo de vida de uma página específica. Devem residir no Layout ou Provider raiz."

---
*Assinado: MesaFlow Kernel L6 — Quality Assurance Division*
