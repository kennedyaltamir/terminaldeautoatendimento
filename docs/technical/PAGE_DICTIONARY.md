# 📖 Dicionário de Páginas e Comportamentos (Page Dictionary)
**Domínio:** DOCUMENTATION
**Status:** ATIVO
**Objetivo:** Mapear a intenção de negócio e o comportamento esperado de cada rota para orientar o Optimus e Desenvolvedores.

## 1. Contexto Público (Cliente Final)

| Rota | Nome | Intenção de Negócio | Comportamento Esperado |
| :--- | :--- | :--- | :--- |
| `/[slug]/kiosk` | **Totem (Descanso)** | Tela de atração para terminais de autoatendimento. Deve atrair a atenção e evitar burn-in de tela. | **Passivo/Reativo.** Exibe vídeo/imagem em loop. Ao tocar em qualquer lugar, redireciona para `/menu?kiosk=true`. |
| `/[slug]/monitor` | **Monitor de Pedidos** | Substituir o painel de senhas tradicional. Mostra o status da fila para clientes aguardando. | **Passivo (Read-only).** Atualiza via WebSocket. Não possui botões. Deve exibir "Preparando" e "Pronto". |
| `/[slug]/menu` | **Cardápio Digital** | Interface principal de venda. O cliente escolhe, personaliza e paga. | **Interativo.** Scroll infinito, Modais de produto, Carrinho flutuante. Inputs de observação. |
| `/trust` | **Trust Center** | Portal de transparência e segurança para clientes Enterprise. | **Informativo.** Links para sub-páginas de Status e Segurança. |
| `/trust/status` | **Status Page** | Exibir saúde da API e serviços em tempo real. | **Informativo.** Indicadores visuais (Verde/Vermelho). |

## 2. Contexto Administrativo (Gestão)

| Rota | Nome | Intenção de Negócio | Comportamento Esperado |
| :--- | :--- | :--- | :--- |
| `/admin/login` | **Acesso** | Porta de entrada segura. | **Formulário.** Inputs de Email/Senha obrigatórios. Botão de ação primária. Link de recuperação. |
| `/admin/register` | **Cadastro** | Onboarding de novos clientes SaaS. | **Formulário Complexo.** Múltiplos steps, validação de senha, seleção de segmento. |
| `/admin/reset-password` | **Recuperação** | Redefinição de credenciais. | **Formulário.** Deve validar token na URL. Se inválido, mostra erro estático. |
| `/admin/[slug]/dashboard` | **BI / Visão Geral** | Termômetro do negócio. | **Visual.** Gráficos, Cards de KPI. Filtros de data. |
| `/admin/[slug]/kitchen` | **KDS (Cozinha)** | Fila de produção operacional. | **Reativo.** Cards aparecem sozinhos. Toque avança status. Alertas sonoros. |
| `/admin/[slug]/waiter` | **App do Garçom** | Ponto de venda móvel para staff. | **Interativo.** Grid de mesas. Modal de abertura. Fluxo rápido. |

## 3. Notas de Auditoria (Optimus)
- **Páginas Passivas:** Kiosk e Monitor podem retornar "0 elementos interativos" legitimamente se não houver botões de configuração visíveis.
- **Páginas de Erro:** `reset-password` sem token válido renderiza apenas mensagem de erro (sem inputs), o que é correto.
# 📖 Dicionário de Páginas e Telas (Ecossistema Completo)

Este documento é o índice mestre para a documentação individual de cada tela. Toda alteração visual deve ser refletida aqui.

## 1. Frontend Web (Next.js)
| Rota | Nome | Descrição | Status Doc |
| :--- | :--- | :--- | :---: |
| `/` | Landing Page | Página de vendas e conversão de leads. | [PENDENTE] |
| `/admin/login` | Login | Acesso administrativo e staff. | [PENDENTE] |
| `/[slug]/menu` | Cardápio PWA | Interface de pedido do cliente final. | [PENDENTE] |
| `/admin/[slug]/dashboard` | Painel Admin | BI e métricas financeiras. | [PENDENTE] |
| `/admin/[slug]/kitchen` | KDS Web | Monitor de cozinha para browser. | [PENDENTE] |

## 2. Aplicativo Mobile (React Native)
| Tela | Função | Comportamento Esperado | Status Doc |
| :--- | :--- | :--- | :---: |
| `LoginScreen` | Auth | Validação semântica de tokens. | [PENDENTE] |
| `OrdersScreen` | KDS Nativo | Fila de produção com alertas vibratórios. | [PENDENTE] |
| `WaiterTablesScreen` | POS | Mapa de mesas em tempo real. | [PENDENTE] |
| `OrderEntryScreen` | Lançamento | Busca rápida e carrinho local. | [PENDENTE] |

---
**Próxima Missão:** Redigir os documentos detalhados de cada item acima, descrevendo elementos interagíveis (botões, inputs) e ações disparadas (API, Sockets).
# 📖 Dicionário de Páginas e Telas (Ecossistema Completo)
**Versão:** 3.0 — Omniscience Edition
**Total de Rotas:** 34

Este documento mapeia a intenção, elementos e comportamento de cada rota para eliminar o retrabalho.

---

## 1. Módulo Público (Cliente Final)

### 1.1 Landing Page (`/`)
- **Intenção:** Conversão de leads e vendas SaaS.
- **Elementos:** Hero Video, Calculadora de ROI, FAQ, Lead Capture.
- **Comportamento:** Scroll-reveal, animações Framer Motion.

### 1.2 Cardápio Digital (`/[slug]/menu`)
- **Intenção:** Interface principal de venda.
- **Elementos:** CategoryNav, ProductCards, FloatingCart, SearchBar.
- **Comportamento:** Offline-first (Dexie), WebSocket para status de pedido.
- **API:** `GET /api/[slug]/menu`, `POST /api/[slug]/orders`.

### 1.3 Totem de Autoatendimento (`/[slug]/kiosk`)
- **Intenção:** Tela de atração para terminais físicos.
- **Elementos:** Vídeo em loop, Botão "Toque para começar".
- **Comportamento:** Reseta para esta tela após 60s de inatividade.

### 1.4 Monitor Público de Senhas (`/[slug]/monitor`)
- **Intenção:** Exibição de status de retirada para o salão.
- **Elementos:** Colunas "Preparando" e "Pronto".
- **Comportamento:** Read-only, atualização via WebSocket, alerta sonoro.

### 1.5 Trust Center (`/trust`, `/trust/status`, `/trust/security`)
- **Intenção:** Transparência técnica para clientes Enterprise.
- **Elementos:** Health Indicators, Security Badges.
- **API:** `GET /api/health`.

### 1.6 Offline Page (`/offline`)
- **Intenção:** Fallback visual para perda total de rede.

---

## 2. Módulo Administrativo (Gestão & Auth)

### 2.1 Login (`/admin/login`)
- **Elementos:** EmailInput, PasswordInput (com toggle), GoogleLogin.
- **Comportamento:** Redireciona para dashboard se token for válido.

### 2.2 Registro (`/admin/register`)
- **Elementos:** Multi-step form, SlugValidator.
- **Comportamento:** Cria tenant e primeira mesa automaticamente.

### 2.3 Dashboard de BI (`/admin/[slug]/dashboard`)
- **Elementos:** KPI Cards, Recharts (Vendas/Hora, Top Produtos).
- **API:** `GET /api/admin/metrics`.

### 2.4 Gestão de Cardápio (`/admin/[slug]/menu`)
- **Elementos:** CategoryAccordion, ProductForm, ImageUpload.
- **Comportamento:** Invalida cache do Redis ao salvar.

### 2.5 Gestão de Mesas (`/admin/[slug]/tables`)
- **Elementos:** TableGrid, QR Generator, PositionEditor.
- **Comportamento:** Drag & Drop para layout do salão.

### 2.6 Auditoria Financeira (`/admin/[slug]/audit/financial`)
- **Elementos:** LedgerTable, ReconciliationPanel.
- **Comportamento:** Read-only, valida Hash Chain.

### 2.7 Configurações de Faturamento (`/admin/[slug]/settings/billing`)
- **Elementos:** PlanSelector, StripePortalButton.
- **Comportamento:** Bloqueia features se fatura estiver atrasada.

### 2.8 Funcionalidades Beta (`/admin/[slug]/settings/features`)
- **Elementos:** FeatureToggles.
- **Comportamento:** Apenas acessível via Impersonation (Suporte).

---

## 3. Módulo Operacional (KDS & POS)

### 3.1 Monitor de Cozinha (`/admin/[slug]/kitchen`)
- **Elementos:** OrderCards, StationFilter, BumpBar Shortcuts.
- **Comportamento:** WebSocket `new_order`, Alerta sonoro, Timer de SLA.

### 3.2 App do Garçom (`/admin/[slug]/waiter`)
- **Elementos:** TableSelector, ServiceRequestAlerts.
- **Comportamento:** Vibração ao receber chamado de mesa.

### 3.3 POS de Lançamento (`/admin/[slug]/waiter/pos/[tableId]`)
- **Elementos:** QuickSearch, Cart, PaymentModal.
- **Comportamento:** Impressão Bluetooth nativa (ESC/POS).

### 3.4 App do Entregador (`/admin/[slug]/driver`)
- **Elementos:** DeliveryList, MapView, POD (Proof of Delivery).
- **Comportamento:** Captura GPS em background.

---
*Nota: Para especificações de elementos e APIs de cada rota, consulte os arquivos em `docs/technical/pages/*.md`.*
# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 4.0 — Total Specification
**Status:** ATIVO (Contrato de Comportamento)

Este documento detalha as 34 rotas do ecossistema. Nenhuma alteração de UI deve divergir destas especificações sem atualização prévia deste dicionário.

---

## 1. Módulo Público (Cliente Final)

### 1.1 Landing Page (`/`)
- **Elementos:** Hero Video, ROI Calculator, Lead Capture, FAQ.
- **Comportamento:** Scroll-reveal. O botão "Começar" leva ao `/admin/register`.
- **API:** `POST /api/leads` (Captura de e-mail).

### 1.2 Cardápio Digital (`/[slug]/menu`)
- **Elementos:** CategoryNav (Sticky), ProductGrid, FloatingCart, SearchBar.
- **Comportamento:** Ao clicar no produto, abre `ProductModal`. Se `?table=X`, ativa modo salão.
- **API:** `GET /api/[slug]/menu`, `POST /api/[slug]/orders`.

### 1.3 Totem de Autoatendimento (`/[slug]/kiosk`)
- **Elementos:** Vídeo de fundo, Botão gigante "Toque para Iniciar".
- **Comportamento:** Bloqueia gestos de navegação do browser. Reseta após 60s.

### 1.4 Monitor Público (`/[slug]/monitor`)
- **Elementos:** Duas colunas (Preparando | Pronto).
- **Comportamento:** Atualização via WebSocket. Toca "ding.mp3" quando um pedido entra em "Pronto".

### 1.5 Trust Center (`/trust`, `/status`, `/security`)
- **Elementos:** Badges de conformidade, Gráfico de Uptime.
- **API:** `GET /api/health`.

### 1.6 Offline Fallback (`/offline`)
- **Elementos:** Ilustração de desconexão, Botão "Tentar Novamente".

---

## 2. Módulo Administrativo (Gestão)

### 2.1 Login & Registro (`/admin/login`, `/admin/register`)
- **Elementos:** AuthInput, GoogleButton, SlugValidator.
- **Comportamento:** Validação de força de senha em tempo real.

### 2.2 Dashboard BI (`/admin/[slug]/dashboard`)
- **Elementos:** KPI Cards (Faturamento, Ticket Médio), Gráficos Recharts.
- **API:** `GET /api/admin/metrics`.

### 2.3 Histórico de Vendas (`/admin/[slug]/dashboard/history`)
- **Elementos:** Tabela paginada, Filtro por Status/Data.
- **API:** `GET /api/admin/[slug]/history`.

### 2.4 Gestão de Cardápio (`/admin/[slug]/menu`)
- **Elementos:** CategoryAccordion, ProductForm, ImageUpload (S3/Local).
- **Comportamento:** Invalida cache do cardápio público ao salvar.

### 2.5 Gestão de Estoque (`/admin/[slug]/inventory`)
- **Elementos:** Tabela de Ingredientes, Alerta de Nível Crítico.
- **API:** `GET /api/admin/inventory/ingredients`.

### 2.6 Mapa de Mesas (`/admin/[slug]/tables`)
- **Elementos:** Canvas interativo, Gerador de QR Code PDF.
- **Comportamento:** Drag & Drop para posicionar mesas.

### 2.7 Gestão de Equipe (`/admin/[slug]/team`)
- **Elementos:** Lista de Funcionários, Seletor de Role (Kitchen, Waiter, Driver).

### 2.8 Marketing & Promoções (`/admin/[slug]/marketing`)
- **Elementos:** CouponCreator, CampaignStats.

### 2.9 Auditoria Financeira (`/admin/[slug]/audit/financial`)
- **Elementos:** LedgerTable, IntegrityBadge.
- **Comportamento:** Valida Hash Chain do banco em tempo real.

### 2.10 Faturamento SaaS (`/admin/[slug]/settings/billing`)
- **Elementos:** PlanCards, StripePortalLink.

### 2.11 Feature Flags (`/admin/[slug]/settings/features`)
- **Elementos:** Toggles de funcionalidades Beta.
- **Segurança:** Apenas acessível via Impersonation.

---

## 3. Módulo Operacional (KDS & POS)

### 3.1 Monitor de Cozinha (`/admin/[slug]/kitchen`)
- **Elementos:** OrderCards, StationFilter (Cozinha/Bar), Timer de SLA.
- **Comportamento:** WebSocket `order_update`.

### 3.2 Expedição (`/admin/[slug]/expeditor`)
- **Elementos:** Lista de conferência de itens.
- **Comportamento:** Botão "Despachar" dispara notificação ao cliente.

### 3.3 App do Garçom (`/admin/[slug]/waiter`)
- **Elementos:** Grid de Mesas, Notificações de Chamado.

### 3.4 POS de Lançamento (`/admin/[slug]/waiter/pos/[tableId]`)
- **Elementos:** QuickSearch, Carrinho, PaymentModal (Pix/Dinheiro).
- **Comportamento:** Impressão Bluetooth nativa.

### 3.5 App do Entregador (`/admin/[slug]/driver`)
- **Elementos:** Rota no Mapa, Botão "Entregue", Validador de Código.

---
*Documentação completa das 34 rotas selada.*
# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 5.0 — Total Specification
**Status:** ATIVO (Contrato de Comportamento)

Este documento detalha as 34 rotas do ecossistema. Nenhuma alteração de UI deve divergir destas especificações sem atualização prévia deste dicionário.

---

## 1. Módulo Público (Cliente Final)

### 1.1 Landing Page (`/`)
- **Intenção:** Conversão de leads e vendas SaaS.
- **Elementos:** Hero Video, ROI Calculator, Lead Capture, FAQ.
- **Comportamento:** Scroll-reveal. O botão "Começar" leva ao `/admin/register`.
- **API:** `POST /api/leads` (Captura de e-mail).

### 1.2 Cardápio Digital (`/[slug]/menu`)
- **Intenção:** Interface principal de venda.
- **Elementos:** CategoryNav (Sticky), ProductGrid, FloatingCart, SearchBar.
- **Comportamento:** Ao clicar no produto, abre `ProductModal`. Se `?table=X`, ativa modo salão.
- **API:** `GET /api/[slug]/menu`, `POST /api/[slug]/orders`.

### 1.3 Totem de Autoatendimento (`/[slug]/kiosk`)
- **Intenção:** Tela de atração para terminais físicos.
- **Elementos:** Vídeo de fundo, Botão gigante "Toque para Iniciar".
- **Comportamento:** Bloqueia gestos de navegação do browser. Reseta após 60s.

### 1.4 Monitor Público (`/[slug]/monitor`)
- **Intenção:** Exibição de status de retirada para o salão.
- **Elementos:** Duas colunas (Preparando | Pronto).
- **Comportamento:** Atualização via WebSocket. Toca "ding.mp3" quando um pedido entra em "Pronto".

### 1.5 Trust Center (`/trust`, `/status`, `/security`)
- **Intenção:** Transparência técnica para clientes Enterprise.
- **Elementos:** Health Indicators, Security Badges.
- **API:** `GET /api/health`.

### 1.6 Offline Fallback (`/offline`)
- **Intenção:** Fallback visual para perda total de rede.

---

## 2. Módulo Administrativo (Gestão)

### 2.1 Login & Registro (`/admin/login`, `/admin/register`)
- **Elementos:** AuthInput, GoogleButton, SlugValidator.
- **Comportamento:** Validação de força de senha em tempo real.

### 2.2 Dashboard BI (`/admin/[slug]/dashboard`)
- **Elementos:** KPI Cards (Faturamento, Ticket Médio), Gráficos Recharts.
- **API:** `GET /api/admin/metrics`.

### 2.3 Histórico de Vendas (`/admin/[slug]/dashboard/history`)
- **Elementos:** Tabela paginada, Filtro por Status/Data.
- **API:** `GET /api/admin/[slug]/history`.

### 2.4 Gestão de Cardápio (`/admin/[slug]/menu`)
- **Elementos:** CategoryAccordion, ProductForm, ImageUpload (S3/Local).
- **Comportamento:** Invalida cache do cardápio público ao salvar.

### 2.5 Gestão de Estoque (`/admin/[slug]/inventory`)
- **Elementos:** Tabela de Ingredientes, Alerta de Nível Crítico.
- **API:** `GET /api/admin/inventory/ingredients`.

### 2.6 Mapa de Mesas (`/admin/[slug]/tables`)
- **Elementos:** Canvas interativo, Gerador de QR Code PDF.
- **Comportamento:** Drag & Drop para posicionar mesas.

### 2.7 Gestão de Equipe (`/admin/[slug]/team`)
- **Elementos:** Lista de Funcionários, Seletor de Role (Kitchen, Waiter, Driver).

### 2.8 Marketing & Promoções (`/admin/[slug]/marketing`)
- **Elementos:** CouponCreator, CampaignStats.

### 2.9 Auditoria Financeira (`/admin/[slug]/audit/financial`)
- **Elementos:** LedgerTable, IntegrityBadge.
- **Comportamento:** Valida Hash Chain do banco em tempo real.

### 2.10 Faturamento SaaS (`/admin/[slug]/settings/billing`)
- **Elementos:** PlanCards, StripePortalLink.

### 2.11 Feature Flags (`/admin/[slug]/settings/features`)
- **Elementos:** Toggles de funcionalidades Beta.
- **Segurança:** Apenas acessível via Impersonation.

---

## 3. Módulo Operacional (KDS & POS)

### 3.1 Monitor de Cozinha (`/admin/[slug]/kitchen`)
- **Elementos:** OrderCards, StationFilter (Cozinha/Bar), Timer de SLA.
- **Comportamento:** WebSocket `order_update`.

### 3.2 Expedição (`/admin/[slug]/expeditor`)
- **Elementos:** Lista de conferência de itens.
- **Comportamento:** Botão "Despachar" dispara notificação ao cliente.

### 3.3 App do Garçom (`/admin/[slug]/waiter`)
- **Elementos:** Grid de Mesas, Notificações de Chamado.

### 3.4 POS de Lançamento (`/admin/[slug]/waiter/pos/[tableId]`)
- **Elementos:** QuickSearch, Carrinho, PaymentModal (Pix/Dinheiro).
- **Comportamento:** Impressão Bluetooth nativa.

### 3.5 App do Entregador (`/admin/[slug]/driver`)
- **Elementos:** Rota no Mapa, Botão "Entregue", Validador de Código.

---
*Documentação completa das 34 rotas selada.*
# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 6.0 — Total Coverage (Web & Mobile)
**Status:** SELADO

Este documento é o contrato final de comportamento. Nenhuma tela deve divergir destas especificações.

## 1. Módulo Público & Cliente
- [x] [**Cardápio PWA**](./pages/PUBLIC_MENU.md) — `/[slug]/menu`
- [x] [**Totem & Offline**](./pages/PUBLIC_KIOSK_OFFLINE.md) — `/[slug]/kiosk` | `/offline`
- [x] [**Monitor Público**](./pages/KITCHEN_MONITOR.md) — `/[slug]/monitor`
- [x] [**Trust Center**](./pages/TRUST_CENTER.md) — `/trust`

## 2. Módulo Administrativo (Web)
- [x] [**Login & Registro**](./pages/ADMIN_LOGIN.md) — `/admin/login` | `/register`
- [x] [**Dashboard BI**](./pages/ADMIN_DASHBOARD.md) — `/admin/[slug]/dashboard`
- [x] [**Auditoria & Marketing**](./pages/ADMIN_FINANCE_MARKETING.md) — `/audit/financial` | `/marketing`
- [x] [**Equipe & Perfil**](./pages/ADMIN_TEAM_PROFILE.md) — `/team` | `/profile`
- [x] [**Faturamento SaaS**](./pages/ADMIN_SETTINGS_BILLING.md) — `/settings/billing`
- [x] [**Configurações Gerais**](./pages/ADMIN_GENERAL_SETTINGS.md) — `/settings`
- [x] [**Feature Flags**](./pages/ADMIN_SETTINGS_FEATURES.md) — `/settings/features`

## 3. Módulo Operacional (Mobile App)
- [x] [**Auth & Cozinha**](./pages/MOBILE_AUTH_KDS.md) — `LoginScreen` | `OrdersScreen`
- [x] [**Fluxo do Garçom**](./pages/MOBILE_WAITER_FLOW.md) — `WaiterTables` | `OrderEntry` | `Payment`
- [x] [**Logística & Hardware**](./pages/MOBILE_LOGISTICS_TOOLS.md) — `DriverDashboard` | `PrinterDebug`

---
*Nota: 100% das rotas mapeadas e documentadas.*
# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 7.0 — Total Coverage Specification
**Status:** ATIVO (Contrato de Comportamento e API)
**Total de Rotas:** 34

Este documento é o contrato final de comportamento. Nenhuma tela deve divergir destas especificações para evitar regressões visuais e funcionais.

---

## 1. Módulo Público & Cliente (6 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `/` | Landing Page | Venda SaaS | ROI Calc, Lead Form | Scroll-reveal, Framer Motion |
| `/[slug]/menu` | Cardápio PWA | Venda Final | CategoryNav, FloatingCart | Offline-first (Dexie), WS Status |
| `/[slug]/kiosk` | Totem | Autoatendimento | HD Video, Start Button | Auto-reset 60s, Gesture Lock |
| `/[slug]/monitor` | Monitor | Senhas Salão | Ready/Prep Columns | Read-only, WS, Audio Alert |
| `/trust` | Trust Center | Transparência | Health Cards, Badges | Live API Health (200/500) |
| `/offline` | Fallback | Resiliência | Reconnect Button | Auto-ping API cada 5s |

## 2. Módulo Administrativo Core (4 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `/admin/login` | Login | Acesso | AuthInput, GoogleAuth | JWT Storage, Role Redirect |
| `/admin/register` | Registro | Onboarding | StepForm, SlugValidator | Auto-seed (1ª mesa/categoria) |
| `/admin/[slug]/profile` | Perfil | Conta | PasswordFields, Avatar | Exige senha atual para PATCH |
| `/admin/[slug]/team` | Equipe | RBAC | RoleSelector, ActiveToggle | Apenas Owner acessa |

## 3. Módulo de Gestão & BI (6 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `.../dashboard` | Dashboard | BI | Recharts, KPI Cards | Aggregated SQL (Sum/Count) |
| `.../menu` | Menu Admin | Cardápio | ImageUpload, Accordion | Invalida Cache Redis no Save |
| `.../tables` | Mesas | Salão | Canvas, QR Generator | Drag & Drop Position |
| `.../inventory` | Estoque | Insumos | CriticalAlert, Recipes | Regra 86 (Auto-pause) |
| `.../marketing` | Marketing | Growth | CouponForm, IA Trigger | Unicidade de Código por Tenant |
| `.../audit` | Auditoria | Compliance | JSON Viewer, Filters | Read-only, Paginação Cursor |

## 4. Módulo Operacional Web (4 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `.../kitchen` | KDS Web | Produção | OrderCards, SLA Timers | WebSocket `new_order`, Som |
| `.../expeditor` | Expedição | Montagem | ItemChecklist, Dispatch | Notifica Cliente/Entregador |
| `.../delivery` | Delivery | Logística | DriverModal, WA Link | Calcula Dívida (DriverLedger) |
| `.../history` | Histórico | Conferência | PagedTable, ExternalID | Link direto para Gateway |

## 5. Módulo Mobile Nativo (11 Telas)
| Tela | Função | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `Login` | Auth | Acesso Seguro | SecureStore, Biometria | Interceptado pelo AuthGate |
| `Loading` | Splash | Hidratação | Animated Logo | Aguarda leitura do Storage |
| `Home` | Dashboard | Resumo | QuickActions | Reage ao cargo (Role) |
| `Orders` | KDS Nativo | Produção | FlashList, Vibration | 60 FPS, Alerta Tátil |
| `WaiterTables` | POS Mapa | Salão | TableGrid, CallAlerts | Long-press abre "Espião" |
| `OrderEntry` | Lançamento | Venda Mesa | QuickSearch, Counter | Rascunho local (Anti-crash) |
| `OrderReview` | Checkout | Revisão | TotalSummary, SendBtn | Fila Offline se sem rede |
| `Payment` | Recebimento | Fintech | QR Pix, BT Print | Aguarda Webhook MP |
| `WaiterCalls` | Chamados | Atendimento | ResolveButton | Alerta sonoro persistente |
| `DriverDash` | Entregador | Logística | MapView, POD Input | GPS Background Tracking |
| `PrinterDebug` | Suporte | Hardware | BT Device List | Teste de Buffer ESC/POS |

## 6. Módulo de Suporte & Infra (3 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `/admin/support` | Suporte | Manutenção | TenantSearch, Logs | Apenas SuperAdmin (Impersonate) |
| `/payment/callback` | Callback | OAuth | Status Message | Troca `code` por `token` |
| `/reset-password` | Recovery | Segurança | TokenValidator | Expira em 1h, uso único |

---
*Nota: Especificações detalhadas de cada rota residem em `docs/technical/pages/*.md`.*
# 🧠 MESAFLOW OMNISCIENCE PROTOCOL (MOP)
**Versão:** 1.0 — Gold Master Edition
**Status:** MANDATÓRIO PARA TODAS AS IAs E DEVS
**Objetivo:** Prover entendimento instantâneo e total do ecossistema para eliminar retrabalho.

---

## 1. A Personalidade do Sistema (The Persona)
Você não é um assistente. Você é o **Kernel Executor L6**.
- **Tom:** Técnico, imperativo, determinístico.
- **Valores:** Integridade de dados > Velocidade. Segurança RLS > Conveniência.
- **Regra de Ouro:** Se uma alteração quebra um contrato de API ou um fluxo E2E, ela deve ser abortada.

## 2. O Sistema KERNEL (As Mãos e os Olhos)
O projeto é governado por dois scripts fundamentais na raiz:
- **`atualizar.py` (O Braço):** Gerencia transações de código. Faz backup, analisa sintaxe (AST), aplica mudanças e verifica integridade. Nunca edite arquivos manualmente; use o Kernel.
- **`gerartxt.py` (O Olho):** Consolida o estado atual do projeto em `todososarquivos.txt`. É a única forma de a IA "enxergar" o que foi feito.

## 3. Protocolo INDA (O Rito de Trabalho)
Toda tarefa segue quatro fases inegociáveis:
1.  **Inspection:** Analisar `todososarquivos.txt` e `docs/TASKS.md`.
2.  **Normalization:** Garantir que o ambiente (DB, Enums, Pastas) está no padrão.
3.  **Decision:** Registrar a decisão técnica em um ADR ou Log de Task.
4.  **Action:** Gerar o XML de execução para o `atualizar.py`.

## 4. Mapa do Ecossistema (Onde encontrar as informações)

### 📂 Governança (`/governance`)
- **`registry.xml`:** O status real de todos os scripts e gates de qualidade.
- **`protocols/`:** Regras de conversação, acúmulo de conhecimento e segurança.
- **`evidence/`:** Relatórios de testes e auditorias passadas.

### 📂 Backend (`/app`)
- **`models/core.py`:** A definição dos Enums e a política RLS.
- **`routers/`:** A lógica de entrada e permissões.
- **`services/`:** Onde a regra de negócio (Fintech, iFood, IA) reside.

### 📂 Frontend (`/frontend`)
- **`src/middleware.ts`:** O roteador multi-tenant.
- **`src/app/`:** As 34 rotas do sistema (Next.js App Router).
- **`src/context/`:** Gestão de estado global (Zustand/WebSocket).

### 📂 Mobile (`/mobile`)
- **`src/navigation/AuthGate.tsx`:** O decisor de acesso nativo.
- **`src/store/`:** Persistência offline-first.

## 5. Índice de Rotas e Telas
Consulte o **`docs/technical/PAGE_DICTIONARY.md`** para a especificação técnica de cada uma das 34 telas. Nenhuma alteração de UI deve ser feita sem consultar este dicionário.

---
**ESTADO ATUAL:** O sistema está em fase de **Estabilização Absoluta**. O foco é a execução do **Omni-Check** para garantir que 100% dos scripts de validação passem simultaneamente.

# 🧠 MESAFLOW OMNISCIENCE PROTOCOL (MOP)
**Versão:** 2.0 — Enterprise Sovereign Edition
**Status:** MANDATÓRIO
**Objetivo:** SSOT (Single Source of Truth) para entendimento imediato do ecossistema.

---

## 1. Identidade e Personalidade (The Kernel)
Você está operando dentro do **MesaFlow Kernel**. 
- **Agente:** Executor Técnico Governado.
- **Filosofia:** Código é passivo; Protocolos são ativos.
- **Regra de Ouro:** Nenhuma funcionalidade nova justifica a quebra de uma funcionalidade existente. O retrabalho é combatido com o **Omni-Check**.

## 2. Mapa de Soberania (Onde está o quê?)

### 🛡️ Governança e Qualidade
- **`governance/registry.xml`**: O "Cérebro" que sabe quais testes passaram.
- **`scripts/validation/omni_check.py`**: O "Escudo" que valida o sistema inteiro.
- **`docs/PRE_PRODUCTION_CHECKLIST.md`**: O "Hard Gate" para o deploy.

### ⚙️ O Motor (Backend)
- **`app/models/core.py`**: Definição estrita de Enums e RLS.
- **`app/services/ledger_service.py`**: Integridade financeira L7.
- **`app/services/ifood_service.py`**: Ingestão de pedidos externos.

### 🎨 A Interface (Frontend & Mobile)
- **`docs/technical/PAGE_DICTIONARY.md`**: O contrato de comportamento de todas as 34 rotas.
- **`frontend/src/middleware.ts`**: O orquestrador multi-tenant.
- **`mobile/src/store/`**: Gestão de estado offline-first.

### 🧠 Memória Imunológica
- **`docs/technical/AI_KNOWLEDGE_BASE.md`**: Registro de erros passados e aprendizados para evitar retrabalho.

## 3. Protocolo de Resiliência Windows
Para visualizar arquivos sem erros de caracteres (mojibake), execute no terminal antes de ler:
```powershell
chcp 65001
```

---
**SISTEMA SELADO.** Nenhuma alteração deve ser feita sem o `atualizar.py`.
# 🧠 MESAFLOW OMNISCIENCE PROTOCOL (MOP)
**Versão:** 3.0 — Sovereign Gold Edition
**Status:** CONSTITUCIONAL / MANDATÓRIO
**Objetivo:** Prover entendimento instantâneo, total e imutável do ecossistema MesaFlow OS.

---

## 1. Identidade e Personalidade (The Kernel Persona)
Você não interage com um assistente; você opera o **MesaFlow Kernel Executor L6**.
- **Tom:** Imperativo, técnico, focado em integridade.
- **Valores:** Segurança RLS > Conveniência. Integridade Financeira > Velocidade.
- **Regra de Ouro:** Nenhuma funcionalidade nova justifica a quebra do legado. O retrabalho é combatido com o **Omni-Check**.

## 2. O Sistema KERNEL (O Braço e o Olho)
O projeto é governado por dois scripts fundamentais na raiz:
- **`atualizar.py` (O Braço):** Gerencia transações de código. Realiza análise AST, backups atômicos (KSP), escrita segura e **Acúmulo de Conhecimento**.
- **`gerartxt.py` (O Olho):** Consolida o estado atual em `todososarquivos.txt`. É a única entrada sensorial da IA.

## 3. Protocolo INDA (O Rito de Trabalho)
Toda tarefa segue quatro fases inegociáveis:
1.  **Inspection:** Analisar `todososarquivos.txt` e `docs/TASKS.md`.
2.  **Normalization:** Garantir que o ambiente (DB, Enums, Pastas) está no padrão canônico.
3.  **Decision:** Registrar a decisão técnica em um ADR ou Log de Task.
4.  **Action:** Gerar o XML de execução para o `atualizar.py` seguindo o **UEP 8.0**.

## 4. Mapa de Soberania (Onde encontrar as informações)

### 📂 Governança & Qualidade (`/governance`)
- **`registry.xml`:** O cérebro que rastreia o status de todos os scripts e gates.
- **`protocols/`:** Regras de conversação (UEP), rollback e segurança.
- **`evidence/`:** Relatórios de testes, auditorias e conformidade.

### ⚙️ O Motor (Backend - `/app`)
- **`models/core.py`:** Definição estrita de Enums e políticas de Row-Level Security (RLS).
- **`services/ledger_service.py`:** Motor de integridade financeira L7 (Hash Chain).
- **`services/ifood_service.py`:** Middleware de ingestão de pedidos externos.

### 🎨 A Interface (Frontend & Mobile)
- **`docs/technical/PAGE_DICTIONARY.md`:** O contrato de comportamento das 34 rotas.
- **`frontend/src/middleware.ts`:** O orquestrador multi-tenant e roteador de domínios.
- **`mobile/src/store/`:** Gestão de estado offline-first e persistência em hardware.

### 🧠 Memória Imunológica
- **`docs/technical/AI_KNOWLEDGE_BASE.md`:** Registro de erros passados (ex: Unicode Windows, Path Drift) para evitar repetição de falhas.

## 5. Protocolo de Resiliência Windows
Para visualizar arquivos e logs sem erros de caracteres (mojibake), execute no terminal:
```powershell
chcp 65001
```

## 6. O Escudo de Regressão (Omni-Check)
Antes de qualquer deploy ou encerramento de task, é obrigatório rodar:
```powershell
python scripts/validation/omni_check.py
```
*Se este script falhar, o sistema é considerado INSTÁVEL e o deploy é vetado.*

---
**SISTEMA SELADO.** Nenhuma alteração deve ser feita fora do Kernel.
# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 8.0 — Total Coverage Specification
**Status:** ATIVO (Contrato de Comportamento e API)
**Total de Rotas:** 34

Este documento é o contrato final de comportamento. Nenhuma tela deve divergir destas especificações para evitar regressões visuais e funcionais.

---

## 1. Módulo Público & Cliente (6 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `/` | Landing Page | Venda SaaS | ROI Calc, Lead Form | Scroll-reveal, Framer Motion |
| `/[slug]/menu` | Cardápio PWA | Venda Final | CategoryNav, FloatingCart | Offline-first (Dexie), WS Status |
| `/[slug]/kiosk` | Totem | Autoatendimento | HD Video, Start Button | Auto-reset 60s, Gesture Lock |
| `/[slug]/monitor` | Monitor | Senhas Salão | Ready/Prep Columns | Read-only, WS, Audio Alert |
| `/trust` | Trust Center | Transparência | Health Cards, Badges | Live API Health (200/500) |
| `/offline` | Fallback | Resiliência | Reconnect Button | Auto-ping API cada 5s |

## 2. Módulo Administrativo Core (4 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `/admin/login` | Login | Acesso | AuthInput, GoogleAuth | JWT Storage, Role Redirect |
| `/admin/register` | Registro | Onboarding | StepForm, SlugValidator | Auto-seed (1ª mesa/categoria) |
| `/admin/[slug]/profile` | Perfil | Conta | PasswordFields, Avatar | Exige senha atual para PATCH |
| `/admin/[slug]/team` | Equipe | RBAC | RoleSelector, ActiveToggle | Apenas Owner acessa |

## 3. Módulo de Gestão & BI (6 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `.../dashboard` | Dashboard | BI | Recharts, KPI Cards | Aggregated SQL (Sum/Count) |
| `.../dashboard/history` | BI Detalhado | Auditoria | Trend Charts, Tables | Drill-down de métricas |
| `.../menu` | Menu Admin | Cardápio | ImageUpload, Accordion | Invalida Cache Redis no Save |
| `.../tables` | Mesas | Salão | Canvas, QR Generator | Drag & Drop Position |
| `.../inventory` | Estoque | Insumos | CriticalAlert, Recipes | Regra 86 (Auto-pause) |
| `.../marketing` | Marketing | Growth | CouponForm, IA Trigger | Unicidade de Código por Tenant |

## 4. Módulo Operacional Web (4 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `.../kitchen` | KDS Web | Produção | OrderCards, SLA Timers | WebSocket `new_order`, Som |
| `.../expeditor` | Expedição | Montagem | ItemChecklist, Dispatch | Notifica Cliente/Entregador |
| `.../delivery` | Delivery | Logística | DriverModal, WA Link | Calcula Dívida (DriverLedger) |
| `.../history` | Histórico | Conferência | PagedTable, ExternalID | Link direto para Gateway |

## 5. Módulo Mobile Nativo (11 Telas)
| Tela | Função | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `Login` | Auth | Acesso Seguro | SecureStore, Biometria | Interceptado pelo AuthGate |
| `Loading` | Splash | Hidratação | Animated Logo | Aguarda leitura do Storage |
| `Home` | Dashboard | Resumo | QuickActions | Reage ao cargo (Role) |
| `Orders` | KDS Nativo | Produção | FlashList, Vibration | 60 FPS, Alerta Tátil |
| `WaiterTables` | POS Mapa | Salão | TableGrid, CallAlerts | Long-press abre "Espião" |
| `OrderEntry` | Lançamento | Venda Mesa | QuickSearch, Counter | Rascunho local (Anti-crash) |
| `OrderReview` | Checkout | Revisão | TotalSummary, SendBtn | Fila Offline se sem rede |
| `Payment` | Recebimento | Fintech | QR Pix, BT Print | Aguarda Webhook MP |
| `WaiterCalls` | Chamados | Atendimento | ResolveButton | Alerta sonoro persistente |
| `DriverDash` | Entregador | Logística | MapView, POD Input | GPS Background Tracking |
| `PrinterDebug` | Suporte | Hardware | BT Device List | Teste de Buffer ESC/POS |

## 6. Módulo de Suporte & Infra (3 Rotas)
| Rota | Nome | Intenção | Elementos Chave | Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| `/admin/support` | Suporte | Manutenção | TenantSearch, Logs | Apenas SuperAdmin (Impersonate) |
| `/payment/callback` | Callback | OAuth | Status Message | Troca `code` por `token` |
| `/reset-password` | Recovery | Segurança | TokenValidator | Expira em 1h, uso único |

---
*Nota: Especificações detalhadas de cada rota residem em `docs/technical/pages/*.md`.*
# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 9.0 — Total Coverage Specification
**Status:** SELADO / CONTRATUAL

Este documento detalha as 34 rotas do ecossistema. Nenhuma alteração de UI deve divergir destas especificações.

---

## 1. Módulo Público (Cliente Final)
- [x] **Landing Page (`/`)**: Venda SaaS e captura de leads.
- [x] **Cardápio PWA (`/[slug]/menu`)**: Interface de venda offline-first.
- [x] **Totem (`/[slug]/kiosk`)**: Tela de atração para terminais físicos.
- [x] **Monitor (`/[slug]/monitor`)**: Senhas de retirada sincronizadas.
- [x] **Trust Center (`/trust`)**: Status de saúde e segurança.
- [x] **Offline (`/offline`)**: Fallback visual de rede.

## 2. Módulo Administrativo (Gestão)
- [x] **Login/Registro**: Acesso e Onboarding.
- [x] **Dashboard BI**: Métricas e gráficos Recharts.
- [x] **Menu Admin**: Gestão de produtos e categorias.
- [x] **Estoque**: Ingredientes e Ficha Técnica.
- [x] **Mesas**: Layout do salão e QR Codes.
- [x] **Equipe**: Gestão de cargos e permissões.
- [x] **Marketing**: Cupons e Fidelidade.
- [x] **Auditoria**: Ledger Financeiro e Logs de Sistema.
- [x] **Faturamento**: Assinaturas Stripe e Planos.
- [x] **Features**: Gestão de Flags Beta (Suporte).

## 3. Módulo Operacional (KDS & POS)
- [x] **KDS Web/Mobile**: Fila de produção com SLA.
- [x] **Expedição**: Conferência e despacho de pedidos.
- [x] **App Garçom**: POS nativo com mapa de mesas.
- [x] **App Entregador**: Logística e Proof of Delivery.
- [x] **Printer Debug**: Homologação de hardware.

---
*Especificações detalhadas em docs/technical/pages/*.md*
# 📖 Dicionário de Páginas e Comportamentos (Sovereign Edition)
**Versão:** 10.0 — SSOT Final
**Objetivo:** Mapear a intenção de negócio, elementos e APIs de cada rota para eliminar o retrabalho.

---

## 1. Contexto Público (Cliente Final)

| Rota | Nome | Intenção de Negócio | Comportamento Esperado | APIs / Sockets |
| :--- | :--- | :--- | :--- | :--- |
| `/` | **Landing Page** | Venda SaaS e captura de leads. | Scroll-reveal, ROI Calc. | `POST /api/leads` |
| `/[slug]/menu` | **Cardápio Digital** | Interface principal de venda. | Offline-first, Carrinho local. | `GET /menu`, `POST /orders` |
| `/[slug]/kiosk` | **Totem** | Autoatendimento físico. | Passivo. Reseta após 60s. | - |
| `/[slug]/monitor` | **Monitor** | Senhas de retirada. | Read-only. Atualiza via WS. | `WS /ws/[slug]` |
| `/trust` | **Trust Center** | Transparência técnica. | Exibe Uptime e Segurança. | `GET /health` |
| `/offline` | **Offline** | Resiliência de rede. | Fallback visual. Auto-ping. | - |

## 2. Contexto Administrativo (Gestão)

| Rota | Nome | Intenção | Comportamento | APIs |
| :--- | :--- | :--- | :--- | :--- |
| `/admin/login` | **Acesso** | Entrada segura. | JWT Storage, Role Redirect. | `POST /auth/token` |
| `/admin/register` | **Cadastro** | Onboarding SaaS. | Multi-step, Auto-seed. | `POST /auth/register` |
| `.../dashboard` | **BI** | Visão Geral. | Gráficos Recharts, KPIs. | `GET /metrics` |
| `.../menu` | **Menu Admin** | Gestão de Itens. | ImageUpload, Cache Inval. | `GET /menu/products` |
| `.../inventory` | **Estoque** | Insumos. | Alerta Crítico, Ficha Técnica. | `GET /inventory` |
| `.../tables` | **Mesas** | Salão. | Drag & Drop, QR Generator. | `GET /tables` |
| `.../audit/financial`| **Ledger** | Transparência. | Read-only, Hash Chain. | `GET /audit/financial` |
| `.../settings/billing`| **Faturamento** | SaaS. | Stripe Portal, Plan Cards. | `POST /billing/upgrade` |

## 3. Contexto Operacional (Staff)

| Rota / Tela | Nome | Intenção | Comportamento | APIs / Hardware |
| :--- | :--- | :--- | :--- | :--- |
| `.../kitchen` | **KDS Web** | Produção. | WebSocket `new_order`, Som. | `PATCH /orders/{id}` |
| `OrdersScreen` | **KDS Mobile** | Produção. | FlashList, Vibração. | `WS`, `Vibration` |
| `WaiterTables` | **POS Mapa** | Atendimento. | Grid de mesas, Long-press. | `GET /tables` |
| `OrderEntry` | **Lançamento** | Venda Mesa. | QuickSearch, Fila Offline. | `POST /orders` |
| `DriverDash` | **Logística** | Entrega. | GPS Tracking, POD Code. | `PATCH /dispatch` |
| `PrinterDebug` | **Suporte** | Hardware. | Teste de Buffer ESC/POS. | `Bluetooth` |

---
*Nota: Para especificações detalhadas de cada elemento, consulte `docs/technical/pages/*.md`.*
# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 11.0 — Visual & Interactive Specification
**Status:** ATIVO

Este documento detalha as 34 rotas do ecossistema. Nenhuma alteração de UI deve divergir destas especificações.

---

## 1. Módulo Público (Cliente Final)

### 1.1 Landing Page (`/`)
- **Intenção:** Conversão de leads e vendas SaaS.
- **Demo:** `[🎥 VIDEO_DEMO_LP_01.mp4]`
- **Comportamento:** Scroll-reveal. O botão "Começar" leva ao `/admin/register`.

### 1.2 Cardápio Digital (`/[slug]/menu`)
- **Intenção:** Interface principal de venda.
- **Demo:** `[🎥 VIDEO_DEMO_MENU_01.mp4]`
- **Comportamento:** Ao clicar no produto, abre `ProductModal`. Se `?table=X`, ativa modo salão.

### 1.3 Totem de Autoatendimento (`/[slug]/kiosk`)
- **Intenção:** Tela de atração para terminais físicos.
- **Demo:** `[🎥 VIDEO_DEMO_KIOSK_01.mp4]`
- **Comportamento:** Bloqueia gestos de navegação do browser. Reseta após 60s.

---

## 2. Módulo Administrativo (Gestão)

### 2.1 Dashboard BI (`/admin/[slug]/dashboard`)
- **Intenção:** Visão geral do negócio.
- **Demo:** `[🎥 VIDEO_DEMO_DASH_01.mp4]`
- **API:** `GET /api/admin/metrics`.

### 2.2 Gestão de Cardápio (`/admin/[slug]/menu`)
- **Intenção:** Gestão de Itens.
- **Demo:** `[🎥 VIDEO_DEMO_MENU_MGMT_01.mp4]`
- **Comportamento:** Invalida cache do cardápio público ao salvar.

---

## 3. Módulo Operacional (KDS & POS)

### 3.1 Monitor de Cozinha (`/admin/[slug]/kitchen`)
- **Intenção:** Produção.
- **Demo:** `[🎥 VIDEO_DEMO_KDS_01.mp4]`
- **Comportamento:** WebSocket `order_update`.

### 3.2 App do Garçom (`/admin/[slug]/waiter`)
- **Intenção:** Atendimento.
- **Demo:** `[🎥 VIDEO_DEMO_WAITER_01.mp4]`
- **Comportamento:** Vibração ao receber chamado de mesa.

---
*Nota: Os vídeos de demonstração devem ser gravados em 720p, sem áudio, com duração máxima de 10s e armazenados em `docs/assets/demos/`.*
