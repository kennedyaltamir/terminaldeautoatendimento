# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:35:00
# 🖥️ TrustCenterPage
> **Plataforma:** Web (Next.js 14)
> **Rota:** `/trust`
> **Acesso:** Public
> **Status:** VALIDATED

## 1. Visão Geral
**Propósito:** Portal de transparência. Exibe status do sistema, políticas de segurança e compliance.
**Persona Principal:** Clientes, Leads.

## 2. Estrutura de Interface
- **Layout Pai:** `TrustLayout`.
- **Componentes Chave:**
  - `StatusIndicator`: Semáforo de uptime (API, DB, Frontend).
  - `SecurityBadges`: Selos de LGPD, PCI-DSS.

## 3. Elementos Interativos & Ações
| Elemento | Tipo | Ação | Feedback Visual | Side Effect |
| :--- | :--- | :--- | :--- | :--- |
| `Ver Detalhes` | Link | Navegação | - | Vai para `/trust/status` |

## 4. Estados da Tela
- **Operational:** Tudo verde.
- **Incident:** Alertas de degradação.

## 5. Fluxos de Navegação
1. **Entrada:** Link no rodapé ou direto.

## 6. Regras de Negócio Críticas
- [x] Dados devem ser reais (Healthcheck API).

## 7. Dados & Integração
- **API Endpoints:**
  - `GET /api/health`

