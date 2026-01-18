# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:20:00
# 🚨 Matriz de Prioridade de Documentação de UI
**Data:** 16/01/2026
**Status:** ATIVO

Esta matriz orienta o esforço de documentação e QA, classificando as telas por impacto no negócio e risco operacional.

## 🔴 Nível 1: Crítico (Blocker de Release)
*Telas essenciais para o fluxo de receita e operação básica. Documentação deve ser exaustiva.*

| Tela | Plataforma | Justificativa | Status Doc |
| :--- | :---: | :--- | :---: |
| `LoginScreen` | Mobile | Entrada no app. Sem isso, nada funciona. | ✅ |
| `LoginPage` | Web | Entrada no admin. | ✅ (Novo) |
| `DashboardPage` | Web | Visão do dono. | ✅ (Novo) |
| `KitchenPage` | Web | Operação da cozinha (KDS). | ✅ (Novo) |
| `OrdersScreen` | Mobile | Lista de pedidos do garçom. | ✅ |
| `PaymentScreen` | Mobile | Recebimento de valores (Pix/Card). | ✅ |
| `Checkout/OrderReview` | Mobile | Confirmação de venda. | ✅ |

## 🟡 Nível 2: Alto (Core Features)
*Funcionalidades importantes, mas com workarounds ou menor frequência de uso.*

| Tela | Plataforma | Justificativa | Status Doc |
| :--- | :---: | :--- | :---: |
| `OrdersPage` | Web | Gestão de pedidos (Backup do KDS). | ✅ (Novo) |
| `SettingsPage` | Web | Configuração da loja. | ❌ MISSING |
| `DriverDashboard` | Mobile | Fluxo de entregadores. | ✅ |
| `WaiterTablesScreen` | Mobile | Mapa de mesas. | ✅ |
| `InventoryPage` | Web | Gestão de estoque. | ❌ MISSING |

## 🟢 Nível 3: Médio/Baixo (Suporte & Info)
*Telas informativas, configurações secundárias ou fluxos de exceção.*

| Tela | Plataforma | Justificativa | Status Doc |
| :--- | :---: | :--- | :---: |
| `ProfilePage` | Web | Dados do usuário. | ❌ MISSING |
| `TeamPage` | Web | Gestão de equipe. | ❌ MISSING |
| `TrustCenterPage` | Web | Páginas institucionais. | ❌ MISSING |
| `OfflinePage` | Web | Estado de erro. | ❌ MISSING |
| `LoadingScreen` | Mobile | Estado transitório. | ✅ |

---
**Ação Recomendada:**
1. Validar conteúdo das telas **Nível 1** (Revisão Humana).
2. Gerar documentação automática para **Nível 2** (Próximo Sprint).
3. Manter **Nível 3** como "Best Effort".

