# 📊 Resumo Executivo de Interface (UI/UX)
> **Gerado em:** 16/01/2026 06:45
> **Escopo:** 68 Telas Mapeadas

## 1. Dashboard de Qualidade
| Métrica | Valor | Status |
| :--- | :---: | :---: |
| **Cobertura Ponderada** | **35.7%** | 🔴 Crítico |
| 🚨 Telas Críticas Falhas | 8 | ❌ Ação Imediata |
| 👻 Fantasmas (Código Ausente) | 0 | Documentação aponta para arquivo inexistente |
| 🔗 Fluxos Quebrados | 0 | Links de navegação sem destino claro |

### 🌐 [Acessar Dashboard Interativo (HTML)](./ui_dashboard.html)

## 2. Mapa de Navegação
```mermaid
graph TD
    classDef web fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;
    classDef mobile fill:#fef3c7,stroke:#d97706,stroke-width:2px;
    classDef critical stroke:#ef4444,stroke-width:4px;
    classDef ghost stroke:#9ca3af,stroke-dasharray: 5 5,fill:#f3f4f6;
    AdminAuditPage["⚠️ AdminAuditPage"]:::web
    AdminBillingPage["⚠️ AdminBillingPage"]:::web
    AdminCounterPage["⚠️ AdminCounterPage"]:::web
    AdminDashboardPage["❌ AdminDashboardPage"]:::web,critical
    AdminDeliveryPage["⚠️ AdminDeliveryPage"]:::web
    AdminDriverPage["⚠️ AdminDriverPage"]:::web
    AdminExpeditorPage["⚠️ AdminExpeditorPage"]:::web
    AdminFeaturesPage["⚠️ AdminFeaturesPage"]:::web
    AdminFinancialPage["⚠️ AdminFinancialPage"]:::web
    AdminForgotPasswordPage["⚠️ AdminForgotPasswordPage"]:::web
    AdminFranchisePage["⚠️ AdminFranchisePage"]:::web
    AdminHistoryPage["⚠️ AdminHistoryPage"]:::web
    AdminInventoryPage["⚠️ AdminInventoryPage"]:::web
    AdminKitchenPage["⚠️ AdminKitchenPage"]:::web
    AdminLoginPage["⚠️ AdminLoginPage"]:::web
    AdminMarketingPage["⚠️ AdminMarketingPage"]:::web
    AdminMenuPage["⚠️ AdminMenuPage"]:::web
    AdminOrdersPage["⚠️ AdminOrdersPage"]:::web
    AdminProfilePage["⚠️ AdminProfilePage"]:::web
    AdminRegisterPage["⚠️ AdminRegisterPage"]:::web
    AdminResetPasswordPage["⚠️ AdminResetPasswordPage"]:::web
    AdminSettingsPage["⚠️ AdminSettingsPage"]:::web
    AdminSupportPage["⚠️ AdminSupportPage"]:::web
    AdminTablesPage["⚠️ AdminTablesPage"]:::web
    AdminTeamPage["⚠️ AdminTeamPage"]:::web
    AdminWaiterPage["⚠️ AdminWaiterPage"]:::web
    AuditPage["⚠️ AuditPage"]:::web
    ClientMenuPage["⚠️ ClientMenuPage"]:::web
    CounterPage["❌ CounterPage"]:::web,critical
    DashboardPage["⚠️ DashboardPage"]:::web
    DeliveryPage["⚠️ DeliveryPage"]:::web
    DriverPage["⚠️ DriverPage"]:::web
    ExpeditorPage["⚠️ ExpeditorPage"]:::web
    FranchisePage["⚠️ FranchisePage"]:::web
    InventoryPage["⚠️ InventoryPage"]:::web
    KioskAttractScreen["⚠️ KioskAttractScreen"]:::web
    KitchenPage["❌ KitchenPage"]:::web,critical
    LandingPage["⚠️ LandingPage"]:::web
    LandingPagePage["⚠️ LandingPagePage"]:::web
    LoginPage["⚠️ LoginPage"]:::web
    MarketingPage["⚠️ MarketingPage"]:::web
    OfflinePage["⚠️ OfflinePage"]:::web
    OrdersPage["⚠️ OrdersPage"]:::web
    ProfilePage["⚠️ ProfilePage"]:::web
    PublicMonitorPage["⚠️ PublicMonitorPage"]:::web
    QuickPosPage["⚠️ QuickPosPage"]:::web
    RegisterPage["⚠️ RegisterPage"]:::web
    SettingsPage["⚠️ SettingsPage"]:::web
    SupportPage["⚠️ SupportPage"]:::web
    TablesPage["⚠️ TablesPage"]:::web
    TeamPage["⚠️ TeamPage"]:::web
    TrustCenterPage["⚠️ TrustCenterPage"]:::web
    WaiterPage["⚠️ WaiterPage"]:::web
    WaiterPosPage["⚠️ WaiterPosPage"]:::web
    [tableid]Page["⚠️ [tableid]Page"]:::web
    DriverDashboard["❌ DriverDashboard"]:::mobile,critical
    HomeScreen["⚠️ HomeScreen"]:::mobile
    KitchenDashboard["⚠️ KitchenDashboard"]:::mobile
    LoadingScreen["⚠️ LoadingScreen"]:::mobile
    LoginScreen["❌ LoginScreen"]:::mobile,critical
    OrderEntryScreen["❌ OrderEntryScreen"]:::mobile,critical
    OrderReviewScreen["⚠️ OrderReviewScreen"]:::mobile
    OrdersScreen["⚠️ OrdersScreen"]:::mobile
    PaymentScreen["❌ PaymentScreen"]:::mobile,critical
    PrinterDebugScreen["⚠️ PrinterDebugScreen"]:::mobile
    WaiterCallsScreen["⚠️ WaiterCallsScreen"]:::mobile
    WaiterDashboard["❌ WaiterDashboard"]:::mobile,critical
    WaiterTablesScreen["⚠️ WaiterTablesScreen"]:::mobile
```

## 3. Matriz de Priorização
| Plataforma | Tela | Status | Código Fonte | Sugestões (Top Priority) |
| :--- | :--- | :---: | :--- | :--- |
| **Web** | [AdminDashboardPage](../../../doctelas/web/AdminDashboardPage.md) | 🚨 CRÍTICO (FALHA) | `frontend\src\app\admin\[slug]\dashboard\page.tsx` | Ver detalhes... |
| **Web** | [CounterPage](../../../doctelas/web/CounterPage.md) | 🚨 CRÍTICO (FALHA) | `frontend\src\app\admin\[slug]\counter\page.tsx` | Ver detalhes... |
| **Web** | [KitchenPage](../../../doctelas/web/KitchenPage.md) | 🚨 CRÍTICO (FALHA) | `frontend\src\app\admin\[slug]\kitchen\page.tsx` | Ver detalhes... |
| **Mobile** | [DriverDashboard](../../../doctelas/mobile/DriverDashboard.md) | 🚨 CRÍTICO (FALHA) | `mobile\src\screens\driver\DriverDashboard.tsx` | Ver detalhes... |
| **Mobile** | [LoginScreen](../../../doctelas/mobile/LoginScreen.md) | 🚨 CRÍTICO (FALHA) | `mobile\src\screens\auth\LoginScreen.tsx` | Ver detalhes... |
| **Mobile** | [OrderEntryScreen](../../../doctelas/mobile/OrderEntryScreen.md) | 🚨 CRÍTICO (FALHA) | `mobile\src\screens\waiter\OrderEntryScreen.tsx` | Ver detalhes... |
| **Mobile** | [PaymentScreen](../../../doctelas/mobile/PaymentScreen.md) | 🚨 CRÍTICO (FALHA) | `mobile\src\screens\waiter\PaymentScreen.tsx` | Ver detalhes... |
| **Mobile** | [WaiterDashboard](../../../doctelas/mobile/WaiterDashboard.md) | 🚨 CRÍTICO (FALHA) | `mobile\src\screens\waiter\WaiterDashboard.tsx` | Ver detalhes... |
| **Web** | [AdminAuditPage](../../../doctelas/web/AdminAuditPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\audit\page.tsx` | Ver detalhes... |
| **Web** | [AdminBillingPage](../../../doctelas/web/AdminBillingPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\settings\billing\page.tsx` | Ver detalhes... |
| **Web** | [AdminCounterPage](../../../doctelas/web/AdminCounterPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\counter\page.tsx` | Ver detalhes... |
| **Web** | [AdminDeliveryPage](../../../doctelas/web/AdminDeliveryPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\delivery\page.tsx` | Ver detalhes... |
| **Web** | [AdminDriverPage](../../../doctelas/web/AdminDriverPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\driver\page.tsx` | Ver detalhes... |
| **Web** | [AdminExpeditorPage](../../../doctelas/web/AdminExpeditorPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\expeditor\page.tsx` | Ver detalhes... |
| **Web** | [AdminFeaturesPage](../../../doctelas/web/AdminFeaturesPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\settings\features\page.tsx` | Ver detalhes... |
| **Web** | [AdminFinancialPage](../../../doctelas/web/AdminFinancialPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\audit\financial\page.tsx` | Ver detalhes... |
| **Web** | [AdminForgotPasswordPage](../../../doctelas/web/AdminForgotPasswordPage.md) | ⚠️ Parcial | `frontend\src\app\admin\forgot-password\page.tsx` | Ver detalhes... |
| **Web** | [AdminFranchisePage](../../../doctelas/web/AdminFranchisePage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\franchise\page.tsx` | Ver detalhes... |
| **Web** | [AdminHistoryPage](../../../doctelas/web/AdminHistoryPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\dashboard\history\page.tsx` | Ver detalhes... |
| **Web** | [AdminInventoryPage](../../../doctelas/web/AdminInventoryPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\inventory\page.tsx` | Ver detalhes... |
| **Web** | [AdminKitchenPage](../../../doctelas/web/AdminKitchenPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\kitchen\page.tsx` | Ver detalhes... |
| **Web** | [AdminLoginPage](../../../doctelas/web/AdminLoginPage.md) | ⚠️ Parcial | `frontend\src\app\admin\login\page.tsx` | Ver detalhes... |
| **Web** | [AdminMarketingPage](../../../doctelas/web/AdminMarketingPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\marketing\page.tsx` | Ver detalhes... |
| **Web** | [AdminMenuPage](../../../doctelas/web/AdminMenuPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\menu\page.tsx` | Ver detalhes... |
| **Web** | [AdminOrdersPage](../../../doctelas/web/AdminOrdersPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\waiter\orders\page.tsx` | Ver detalhes... |
| **Web** | [AdminProfilePage](../../../doctelas/web/AdminProfilePage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\profile\page.tsx` | Ver detalhes... |
| **Web** | [AdminRegisterPage](../../../doctelas/web/AdminRegisterPage.md) | ⚠️ Parcial | `frontend\src\app\admin\register\page.tsx` | Ver detalhes... |
| **Web** | [AdminResetPasswordPage](../../../doctelas/web/AdminResetPasswordPage.md) | ⚠️ Parcial | `frontend\src\app\admin\reset-password\page.tsx` | Ver detalhes... |
| **Web** | [AdminSettingsPage](../../../doctelas/web/AdminSettingsPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\settings\page.tsx` | Ver detalhes... |
| **Web** | [AdminSupportPage](../../../doctelas/web/AdminSupportPage.md) | ⚠️ Parcial | `frontend\src\app\admin\support\page.tsx` | Ver detalhes... |
| **Web** | [AdminTablesPage](../../../doctelas/web/AdminTablesPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\tables\page.tsx` | Ver detalhes... |
| **Web** | [AdminTeamPage](../../../doctelas/web/AdminTeamPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\team\page.tsx` | Ver detalhes... |
| **Web** | [AdminWaiterPage](../../../doctelas/web/AdminWaiterPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\waiter\page.tsx` | Ver detalhes... |
| **Web** | [AuditPage](../../../doctelas/web/AuditPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\audit\page.tsx` | Ver detalhes... |
| **Web** | [ClientMenuPage](../../../doctelas/web/ClientMenuPage.md) | ⚠️ Parcial | `frontend\src\app\[slug]\menu\page.tsx` | Ver detalhes... |
| **Web** | [DashboardPage](../../../doctelas/web/DashboardPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\dashboard\page.tsx` | Ver detalhes... |
| **Web** | [DeliveryPage](../../../doctelas/web/DeliveryPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\delivery\page.tsx` | Ver detalhes... |
| **Web** | [DriverPage](../../../doctelas/web/DriverPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\driver\page.tsx` | Ver detalhes... |
| **Web** | [ExpeditorPage](../../../doctelas/web/ExpeditorPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\expeditor\page.tsx` | Ver detalhes... |
| **Web** | [FranchisePage](../../../doctelas/web/FranchisePage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\franchise\page.tsx` | Ver detalhes... |
| **Web** | [InventoryPage](../../../doctelas/web/InventoryPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\inventory\page.tsx` | Ver detalhes... |
| **Web** | [KioskAttractScreen](../../../doctelas/web/KioskAttractScreen.md) | ⚠️ Parcial | `frontend\src\app\[slug]\kiosk\page.tsx` | Ver detalhes... |
| **Web** | [LandingPage](../../../doctelas/web/LandingPage.md) | ⚠️ Parcial | `frontend\src\app\page.tsx` | Ver detalhes... |
| **Web** | [LandingPagePage](../../../doctelas/web/LandingPagePage.md) | ⚠️ Parcial | `frontend\src\app\page.tsx` | Ver detalhes... |
| **Web** | [LoginPage](../../../doctelas/web/LoginPage.md) | ⚠️ Parcial | `frontend\src\app\admin\login\page.tsx` | Ver detalhes... |
| **Web** | [MarketingPage](../../../doctelas/web/MarketingPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\marketing\page.tsx` | Ver detalhes... |
| **Web** | [OfflinePage](../../../doctelas/web/OfflinePage.md) | ⚠️ Parcial | `frontend\src\app\offline\page.tsx` | Ver detalhes... |
| **Web** | [OrdersPage](../../../doctelas/web/OrdersPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\waiter\orders\page.tsx` | Ver detalhes... |
| **Web** | [ProfilePage](../../../doctelas/web/ProfilePage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\profile\page.tsx` | Ver detalhes... |
| **Web** | [PublicMonitorPage](../../../doctelas/web/PublicMonitorPage.md) | ⚠️ Parcial | `frontend\src\app\[slug]\monitor\page.tsx` | Ver detalhes... |
| **Web** | [QuickPosPage](../../../doctelas/web/QuickPosPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\waiter\pos\quick\page.tsx` | Ver detalhes... |
| **Web** | [RegisterPage](../../../doctelas/web/RegisterPage.md) | ⚠️ Parcial | `frontend\src\app\admin\register\page.tsx` | Ver detalhes... |
| **Web** | [SettingsPage](../../../doctelas/web/SettingsPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\settings\page.tsx` | Ver detalhes... |
| **Web** | [SupportPage](../../../doctelas/web/SupportPage.md) | ⚠️ Parcial | `frontend\src\app\admin\support\page.tsx` | Ver detalhes... |
| **Web** | [TablesPage](../../../doctelas/web/TablesPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\tables\page.tsx` | Ver detalhes... |
| **Web** | [TeamPage](../../../doctelas/web/TeamPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\team\page.tsx` | Ver detalhes... |
| **Web** | [TrustCenterPage](../../../doctelas/web/TrustCenterPage.md) | ⚠️ Parcial | `frontend\src\app\trust\page.tsx` | Ver detalhes... |
| **Web** | [WaiterPage](../../../doctelas/web/WaiterPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\waiter\page.tsx` | Ver detalhes... |
| **Web** | [WaiterPosPage](../../../doctelas/web/WaiterPosPage.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\waiter\pos\[tableId]\page.tsx` | Ver detalhes... |
| **Web** | [[tableid]Page](../../../doctelas/web/[tableid]Page.md) | ⚠️ Parcial | `frontend\src\app\admin\[slug]\waiter\pos\[tableId]\page.tsx` | Ver detalhes... |
| **Mobile** | [HomeScreen](../../../doctelas/mobile/HomeScreen.md) | ⚠️ Parcial | `mobile\src\screens\app\HomeScreen.tsx` | Ver detalhes... |
| **Mobile** | [KitchenDashboard](../../../doctelas/mobile/KitchenDashboard.md) | ⚠️ Parcial | `mobile\src\screens\kitchen\KitchenDashboard.tsx` | Ver detalhes... |
| **Mobile** | [LoadingScreen](../../../doctelas/mobile/LoadingScreen.md) | ⚠️ Parcial | `mobile\src\screens\common\LoadingScreen.tsx` | Ver detalhes... |
| **Mobile** | [OrderReviewScreen](../../../doctelas/mobile/OrderReviewScreen.md) | ⚠️ Parcial | `mobile\src\screens\waiter\OrderReviewScreen.tsx` | Ver detalhes... |
| **Mobile** | [OrdersScreen](../../../doctelas/mobile/OrdersScreen.md) | ⚠️ Parcial | `mobile\src\screens\orders\OrdersScreen.tsx` | Ver detalhes... |
| **Mobile** | [PrinterDebugScreen](../../../doctelas/mobile/PrinterDebugScreen.md) | ⚠️ Parcial | `mobile\src\screens\waiter\PrinterDebugScreen.tsx` | Ver detalhes... |
| **Mobile** | [WaiterCallsScreen](../../../doctelas/mobile/WaiterCallsScreen.md) | ⚠️ Parcial | `mobile\src\screens\waiter\WaiterCallsScreen.tsx` | Ver detalhes... |
| **Mobile** | [WaiterTablesScreen](../../../doctelas/mobile/WaiterTablesScreen.md) | ⚠️ Parcial | `mobile\src\screens\waiter\WaiterTablesScreen.tsx` | Ver detalhes... |