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
