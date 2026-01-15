# 🛡️ Análise de Incidente: UI Stress Test (Falha de Conectividade e Permissão)
**Data:** 10 de Janeiro de 2026
**Status:** CRÍTICO
**Origem:** Relatório de Teste Automatizado (v2)

## 1. Resumo Executivo
O teste de estresse da interface revelou uma **falha sistêmica de comunicação entre o Frontend (Next.js) e o Backend (FastAPI)**. Embora a aplicação web carregue (renderize o shell), os dados não estão sendo populados devido a erros de rede e permissão.

A interface está "viva", mas "vazia" ou "quebrada" funcionalmente.

## 2. Diagnóstico Técnico Detalhado

### 🔴 Erro 1: `TypeError: Failed to fetch` (Colapso de API)
**Evidência:**
```text
at fetchClient (src/lib/api.ts:102:26)
at getDashboardMetrics ...
error: Erro ao carregar métricas: ApiError: Servidor indisponível.
```
**Análise:**
O cliente HTTP do frontend (`fetchClient`) não conseguiu estabelecer conexão com `http://127.0.0.1:8000`.
- **Causa Provável A:** O Backend não estava rodando no momento do teste.
- **Causa Provável B:** Bloqueio de CORS ou Firewall impedindo que o `localhost:3000` acesse `127.0.0.1:8000`.
- **Impacto:** Dashboards vazios, KDS sem pedidos, menus sem produtos. O React Server Components (RSC) falha ao tentar renderizar no servidor.

### 🟠 Erro 2: `403 Forbidden` em `/api/admin/delivery/orders`
**Evidência:**
```text
NETWORK: 403 http://127.0.0.1:8000/api/admin/delivery/orders
```
**Análise:**
O usuário autenticado (`admin@mesaflow.com`) tentou acessar o módulo de Delivery, mas o servidor rejeitou.
- **Causa Provável:** O Token JWT gerado no login não possui a *role* ou permissão necessária para acessar a rota de logística, ou o RLS (Row Level Security) bloqueou o acesso por inconsistência de `company_id`.
- **Impacto:** O módulo de Delivery está inacessível para o administrador.

### 🟡 Erro 3: Interferência de UI (Joyride/Overlays)
**Evidência (Logs anteriores):**
```text
<div class="react-joyride__overlay">... intercepts pointer events
```
**Análise:**
O tutorial de onboarding (Joyride) está aparecendo sobre os botões, impedindo que o robô de teste clique nos elementos de navegação.
- **Impacto:** Falsos negativos em testes de interação. O robô tenta clicar, mas clica no overlay transparente do tutorial.

## 3. Plano de Correção (Script v3)

Para resolver e validar definitivamente, o novo script `comprehensive_ui_test_v3.py` implementará:

1.  **Pre-Flight Check:** Verificação de conectividade com a API antes de abrir o navegador.
2.  **Joyride Killer:** Um script injetado no navegador que remove agressivamente o overlay do tutorial do DOM.
3.  **Network Sniffer:** Captura detalhada de *todas* as requisições falhas (não apenas erros de console) para identificar exatamente qual endpoint retorna 403 ou 500.
4.  **Exploração Profunda:** Em vez de apenas clicar no menu, o script tentará interagir com formulários e listas para provar funcionalidade.

---
*Relatório gerado pelo MesaFlow Architect Kernel.*
