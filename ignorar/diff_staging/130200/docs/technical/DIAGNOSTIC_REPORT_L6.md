# 🩺 Relatório de Diagnóstico Profundo: Falha de Estabilidade E2E
**Data:** 15/01/2026
**Status:** CRÍTICO
**Contexto:** Loop de Renderização React & Inconsistência de Estado em Testes

## 1. Resumo Executivo
O sistema apresenta uma falha estrutural na gestão de estado do Frontend, resultando em um **Loop Infinito de Renderização** (`Maximum update depth exceeded`) que causa o crash silencioso do componente `DriverPage` durante a execução de testes automatizados.

A causa raiz não é um "bug simples", mas um **conflito de autoridade de estado**: o Frontend tenta derivar o estado "Ativo" a partir de dados do Backend (via Polling/WebSocket) enquanto simultaneamente tenta impor um estado "Otimista" localmente. Quando esses dois fluxos colidem (especialmente sob a latência de rede simulada ou real), o React entra em ciclo de re-renderização.

## 2. Análise Técnica Detalhada

### A. O Loop da Morte (React Render Cycle)
O erro `Maximum update depth exceeded` ocorre porque um `useEffect` está atualizando um estado (`setOrders` ou `setActiveDeliveryId`) que, por sua vez, é uma dependência direta ou indireta do próprio efeito.

**Ciclo Vicioso Identificado:**
1. **Render:** Componente monta.
2. **Effect:** `useEffect` detecta mudança em `orders`.
3. **Action:** Calcula `activeDeliveryId` baseado em `orders`.
4. **Update:** Chama `setActiveDeliveryId(...)`.
5. **Re-Render:** O componente renderiza novamente.
6. **Effect:** O `fetchOrders` (que depende de `activeDeliveryId` ou é recriado) roda novamente.
7. **Update:** `setOrders` é chamado.
8. **Loop:** Volta para o passo 2.

### B. A Falha do Teste E2E (Playwright)
O teste falha com `element(s) not found` para o painel ativo porque:
1. O componente entra no loop acima e o React aborta a renderização (Crash).
2. O teste executa `page.reload()`. Isso limpa o estado de memória (Zustand/State).
3. Ao recarregar, o Frontend pede dados ao Backend.
4. **Race Condition:** Se o Backend ainda não processou a transição para `delivering` (consistência eventual), ele retorna `ready`.
5. O Frontend renderiza a lista de "Disponíveis" em vez do "Painel Ativo".
6. O teste espera o painel ativo, dá timeout e falha.

### C. Serviços Externos (OSRM/GPS)
O erro `TypeError: Failed to fetch` no OSRM indica que o ambiente de teste (Headless/CI) não tem acesso à rede externa ou o serviço bloqueou a requisição. Isso não deveria quebrar a UI, mas se não houver tratamento de erro (Try/Catch), o componente desmonta.

## 3. Matriz de Inconsistências

| Sintoma | Local | Causa Raiz | Severidade |
| :--- | :--- | :--- | :--- |
| `Maximum update depth` | `DriverPage` (useEffect) | Dependência circular entre `orders` e `activeDeliveryId`. | 🔴 CRÍTICA |
| `element not found` | Teste E2E | Componente crashou ou Estado resetou após Reload. | 🔴 CRÍTICA |
| `Failed to fetch` | `lib/routing.ts` | Falta de Mock para serviços externos em ambiente de teste. | 🟡 MÉDIA |
| `GPS OFF` | UI Header | Dependência de API de Geolocalização não mockada no Playwright. | 🟡 MÉDIA |
| `Flicker` de UI | `fetchOrders` | Substituição total do estado `orders` sem merge inteligente. | 🟡 MÉDIA |

---

## 4. Arquitetura Recomendada (Solução L6)

Para resolver isso definitivamente, aplicaremos o padrão **Canonical State with Smart Merge**:

1.  **Estado Canônico:** O ID do pedido ativo (`activeDeliveryId`) é a fonte de verdade soberana da UI.
2.  **Merge Inteligente:** Ao receber dados do Backend (Polling/WS), não sobrescrevemos cegamente. Se temos um ID ativo localmente, forçamos o status dele para `delivering` na memória, garantindo estabilidade visual até que o Backend confirme.
3.  **Isolamento de Teste:** Detecção de `isTestEnv` para mockar GPS e Rotas, eliminando flakiness de rede.
4.  **Remoção de Reload:** O teste deve confiar na reatividade da UI, não em recarregar a página.

---
*Assinado: Optimus Kernel L6 — Architecture Division*
