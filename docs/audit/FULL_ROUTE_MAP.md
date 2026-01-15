
# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-13 11:45:00
# 🗺️ Mapa Integral de Rotas - MesaFlow OS
**Build:** v1.0 Gold Master
**Status:** Auditado

## 🏢 Contexto Público (Cliente & Institucional)
| Rota | Descrição | Status |
| :--- | :--- | :---: |
| `/` | Landing Page | ✅ 200 |
| `/[slug]/menu` | Cardápio Digital (PWA) | ✅ 200 |
| `/[slug]/kiosk` | Modo Totem | ✅ 200 |
| `/[slug]/monitor` | Telão de Pedidos | ✅ 200 |
| `/trust` | Portal de Transparência | ✅ 200 |
| `/trust/status` | Página de Status de Infra | ✅ 200 |
| `/trust/security` | Políticas de Segurança | ✅ 200 |

## 🔐 Autenticação
| Rota | Descrição | Status |
| :--- | :--- | :---: |
| `/admin/login` | Login Administrativo | ✅ 200 |
| `/admin/register` | Cadastro de Nova Empresa | ✅ 200 |
| `/admin/forgot-password` | Recuperação de Senha | ✅ 200 |
| `/admin/support` | Suporte (God Mode) | 🔒 401 |

## 👔 Administrativo (Gestão)
| Rota | Descrição | Status |
| :--- | :--- | :---: |
| `/admin/[slug]/dashboard` | BI & Métricas | 🔒 401 |
| `/admin/[slug]/menu` | Gestão de Produtos | 🔒 401 |
| `/admin/[slug]/tables` | Gestão de Mesas | 🔒 401 |
| `/admin/[slug]/inventory` | Controle de Estoque | 🔒 401 |
| `/admin/[slug]/audit` | Trilha de Auditoria | 🔒 401 |
| `/admin/[slug]/history` | Histórico de Vendas | 🔒 401 |
| `/admin/[slug]/settings` | Configurações Gerais | 🔒 401 |

## 👨‍🍳 Operacional (Staff)
| Rota | Descrição | Status |
| :--- | :--- | :---: |
| `/admin/[slug]/kitchen` | Monitor KDS | 🔒 401 |
| `/admin/[slug]/waiter` | App do Garçom | 🔒 401 |
| `/admin/[slug]/delivery` | Painel de Logística | 🔒 401 |
| `/admin/[slug]/driver` | App do Entregador | 🔒 401 |
| `/admin/[slug]/expeditor` | Conferência de Pedidos | 🔒 401 |

---
*Mapeamento gerado via Inspeção Estática L6.*

