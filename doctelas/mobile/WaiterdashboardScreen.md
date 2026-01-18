# 🏠 WaiterDashboardScreen
> **Plataforma:** MOBILE | **Domínio:** OPERACIONAL | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
O Dashboard do Garçom é o hub inicial de produtividade. Ele fornece uma visão panorâmica das responsabilidades do funcionário no turno, incluindo suas mesas ativas, total de vendas acumuladas e acesso rápido às ferramentas de lançamento e fechamento.

## 2. Estrutura e Design
- **Performance Widgets:** Cards com métricas pessoais (Total Vendido, Gorjetas Estimadas).
- **Active Sessions Carousel:** Atalhos para as últimas mesas onde o garçom realizou lançamentos.
- **Quick Action Grid:** Botões grandes para "Abrir Nova Mesa", "Lançamento Rápido" e "Ver Chamados".

## 3. Elementos Interativos
- **Profile Switcher:** Acesso às configurações de perfil e logout seguro.
- **Notification Bell:** Indicador visual de chamados pendentes com contador em tempo real.
- **Shift Toggle:** Funcionalidade para iniciar ou encerrar o turno de trabalho (Audit Trail).

## 4. Regras de Negócio
- **Role Enforcement:** A interface adapta os botões visíveis baseada na permissão do usuário (ex: Garçom vs Gerente).
- **Data Hydration:** Carregamento inicial via `useAuthStore` para garantir que o contexto do Tenant (CompanyID) esteja correto.
- **Cache Policy:** Utiliza `AsyncStorage` para manter as métricas visíveis mesmo em zonas de sombra de Wi-Fi.

## 5. Estados e Cenários
- **Loading:** Skeletons circulares para os widgets de performance.
- **Offline Mode:** Banner de "Modo Offline" com acesso restrito apenas a funções de consulta local.
- **Error Boundary:** Captura de falhas de renderização com opção de reinicialização do app.

## 6. Fluxo de Navegação
1. O usuário loga e cai no Dashboard.
2. O sistema valida o cargo e carrega as métricas via `GET /api/admin/metrics/staff`.
3. O garçom seleciona uma ação e transita para a `AppStack`.

---
*MesaFlow Mobile Kernel v5.0*

