# 🔌 MesaFlow Enterprise API v3.3.6
> **Gerado Automaticamente em:** nt.times_result(user=1.78125, system=0.84375, children_user=0.0, children_system=0.0, elapsed=0.0)


# 🚀 MesaFlow API v2.3.0
O Sistema Operacional para Food Service e Ambientes de Alto Tráfego.

## 🔑 Autenticação
A maioria das rotas administrativas requer um token **Bearer JWT**.
Para obter um token, utilize o endpoint `/api/auth/token` ou `/api/auth/google`.

## 📡 WebSockets
Para receber atualizações em tempo real (Novos Pedidos/KDS), conecte-se em:
`ws://{host}/api/ws/{company_slug}`

## 🛡️ Segurança Multi-tenant
Todos os recursos são isolados via `company_id`. 
É impossível acessar dados de uma empresa usando o token de outra.


## POST `/api/auth/logout`
**Resumo:** Logout
**Tags:** Authentication

---

## POST `/api/auth/impersonate`
**Resumo:** Impersonate User
**Tags:** Authentication

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `x-super-secret` | header | ✅ | string |

---

## POST `/api/auth/token`
**Resumo:** Login For Access Token
**Tags:** Authentication

---

## POST `/api/auth/refresh`
**Resumo:** Refresh Token Endpoint
**Tags:** Authentication

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `x-refresh-token` | header | ✅ | string |

---

## POST `/api/auth/google`
**Resumo:** Google Auth
**Tags:** Authentication

---

## POST `/api/auth/register`
**Resumo:** Register Company
**Tags:** Authentication

---

## POST `/api/auth/device`
**Resumo:** Register Device
**Tags:** Authentication

---

## DELETE `/api/auth/device/{token}`
**Resumo:** Unregister Device
**Tags:** Authentication

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `token` | path | ✅ | string |

---

## GET `/api/resolve-domain`
**Resumo:** Resolve Domain
**Tags:** Public API

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `host` | query | ✅ | string |

---

## GET `/api/{company_slug}/menu`
**Resumo:** Get Menu
**Tags:** Public API

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `company_slug` | path | ✅ | string |

---

## GET `/api/{company_slug}/wallet/{phone}`
**Resumo:** Get Customer Wallet
**Tags:** Public API

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `company_slug` | path | ✅ | string |
| `phone` | path | ✅ | string |

---

## POST `/api/{company_slug}/check-table`
**Resumo:** Check Table Status
**Tags:** Public API

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `company_slug` | path | ✅ | string |

---

## POST `/api/{company_slug}/join-table`
**Resumo:** Join Table
**Tags:** Public API

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `company_slug` | path | ✅ | string |

---

## POST `/api/{company_slug}/orders`
**Resumo:** Create Order
**Tags:** Public API

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `company_slug` | path | ✅ | string |

---

## POST `/api/upload/`
**Resumo:** Upload Image
**Tags:** Media & Uploads

---

## GET `/api/admin/features`
**Resumo:** List My Features
**Tags:** Admin - Features

---

## POST `/api/admin/features`
**Resumo:** Update Feature Flag
**Tags:** Admin - Features

---

## GET `/api/admin/{company_slug}/orders`
**Resumo:** Get Kitchen Orders
**Tags:** Admin - Orders

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `company_slug` | path | ✅ | string |

---

## PATCH `/api/admin/orders/{order_id}`
**Resumo:** Update Order Status
**Tags:** Admin - Orders

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `order_id` | path | ✅ | string |

---

## GET `/api/admin/{company_slug}/service-requests`
**Resumo:** Get Service Requests
**Tags:** Admin - Orders

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `company_slug` | path | ✅ | string |

---

## GET `/api/admin/menu/products`
**Resumo:** Get All Products
**Tags:** Admin - Menu

---

## POST `/api/admin/menu/products`
**Resumo:** Create Product
**Tags:** Admin - Menu

---

## POST `/api/admin/menu/categories`
**Resumo:** Create Category
**Tags:** Admin - Menu

---

## PATCH `/api/admin/menu/categories/{category_id}`
**Resumo:** Update Category
**Tags:** Admin - Menu

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `category_id` | path | ✅ | integer |

---

## DELETE `/api/admin/menu/categories/{category_id}`
**Resumo:** Delete Category
**Tags:** Admin - Menu

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `category_id` | path | ✅ | integer |

---

## PATCH `/api/admin/menu/products/{product_id}`
**Resumo:** Update Product
**Tags:** Admin - Menu

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `product_id` | path | ✅ | integer |

---

## DELETE `/api/admin/menu/products/{product_id}`
**Resumo:** Delete Product
**Tags:** Admin - Menu

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `product_id` | path | ✅ | integer |

---

## POST `/api/admin/menu/products/{product_id}/groups`
**Resumo:** Create Option Group
**Tags:** Admin - Menu

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `product_id` | path | ✅ | integer |

---

## POST `/api/admin/menu/groups/{group_id}/options`
**Resumo:** Create Option
**Tags:** Admin - Menu

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `group_id` | path | ✅ | integer |

---

## DELETE `/api/admin/menu/groups/{group_id}`
**Resumo:** Delete Option Group
**Tags:** Admin - Menu

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `group_id` | path | ✅ | integer |

---

## DELETE `/api/admin/menu/options/{option_id}`
**Resumo:** Delete Option
**Tags:** Admin - Menu

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `option_id` | path | ✅ | integer |

---

## POST `/api/admin/menu/import/ifood`
**Resumo:** Import Ifood Menu
**Tags:** Admin - Menu

---

## GET `/api/admin`
**Resumo:** Get Tables
**Tags:** Admin - Tables

---

## POST `/api/admin`
**Resumo:** Create Table
**Tags:** Admin - Tables

---

## GET `/api/admin/{slug}/tables`
**Resumo:** Get Tables By Slug
**Tags:** Admin - Tables, Admin - Tables

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `slug` | path | ✅ | string |

---

## POST `/api/admin/bulk`
**Resumo:** Create Tables Bulk
**Tags:** Admin - Tables

---

## DELETE `/api/admin/{table_id}`
**Resumo:** Delete Table
**Tags:** Admin - Tables

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `table_id` | path | ✅ | integer |

---

## PATCH `/api/admin/positions`
**Resumo:** Update Table Positions
**Tags:** Admin - Tables

---

## GET `/api/admin/dashboard`
**Resumo:** Get Tables Dashboard
**Tags:** Admin - Tables

---

## POST `/api/admin/{table_id}/open`
**Resumo:** Open Table Session
**Tags:** Admin - Tables

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `table_id` | path | ✅ | integer |

---

## POST `/api/admin/{table_id}/pay`
**Resumo:** Pay Table Partial
**Tags:** Admin - Tables

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `table_id` | path | ✅ | integer |

---

## POST `/api/admin/{table_id}/close`
**Resumo:** Close Table Session
**Tags:** Admin - Tables

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `table_id` | path | ✅ | integer |

---

## PATCH `/api/admin/sessions/{session_id}`
**Resumo:** Update Session Name
**Tags:** Admin - Tables

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `session_id` | path | ✅ | integer |

---

## GET `/api/admin/sessions/{session_id}/details`
**Resumo:** Get Session Details
**Tags:** Admin - Tables

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `session_id` | path | ✅ | integer |

---

## POST `/api/admin/transfer`
**Resumo:** Transfer Table
**Tags:** Admin - Tables

---

## GET `/api/admin/inventory/ingredients`
**Resumo:** Get Ingredients
**Tags:** Admin - Inventory

---

## POST `/api/admin/inventory/ingredients`
**Resumo:** Create Ingredient
**Tags:** Admin - Inventory

---

## PATCH `/api/admin/inventory/ingredients/{ingredient_id}`
**Resumo:** Update Ingredient
**Tags:** Admin - Inventory

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `ingredient_id` | path | ✅ | integer |

---

## DELETE `/api/admin/inventory/ingredients/{ingredient_id}`
**Resumo:** Delete Ingredient
**Tags:** Admin - Inventory

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `ingredient_id` | path | ✅ | integer |

---

## POST `/api/admin/inventory/recipes`
**Resumo:** Update Product Recipe
**Tags:** Admin - Inventory

---

## GET `/api/admin/inventory/suppliers`
**Resumo:** Get Suppliers
**Tags:** Admin - Inventory

---

## POST `/api/admin/inventory/suppliers`
**Resumo:** Create Supplier
**Tags:** Admin - Inventory

---

## DELETE `/api/admin/inventory/suppliers/{supplier_id}`
**Resumo:** Delete Supplier
**Tags:** Admin - Inventory

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `supplier_id` | path | ✅ | integer |

---

## GET `/api/admin/inventory/shopping-list`
**Resumo:** Get Shopping List
**Tags:** Admin - Inventory

---

## GET `/api/admin/inventory/purchase-orders/preview`
**Resumo:** Preview Purchase Orders
**Tags:** Admin - Inventory

---

## GET `/api/admin/inventory/purchase-orders/{supplier_id}/print`
**Resumo:** Print Purchase Order
**Tags:** Admin - Inventory

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `supplier_id` | path | ✅ | integer |

---

## GET `/api/admin/delivery/orders`
**Resumo:** Get Delivery Orders
**Tags:** Admin - Logistics

---

## PATCH `/api/admin/delivery/orders/{order_id}/dispatch`
**Resumo:** Dispatch Order
**Tags:** Admin - Logistics

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `order_id` | path | ✅ | string |

---

## PATCH `/api/admin/delivery/orders/{order_id}/complete`
**Resumo:** Complete Delivery
**Tags:** Admin - Logistics

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `order_id` | path | ✅ | string |

---

## GET `/api/admin/logistics/dashboard`
**Resumo:** Get Logistics Dashboard
**Tags:** Admin - Logistics

---

## GET `/api/admin/employees`
**Resumo:** Get Employees
**Tags:** Admin - Team

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `role` | query | ❌ | string |

---

## POST `/api/admin/employees`
**Resumo:** Create Employee
**Tags:** Admin - Team

---

## DELETE `/api/admin/employees/{employee_id}`
**Resumo:** Delete Employee
**Tags:** Admin - Team

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `employee_id` | path | ✅ | integer |

---

## GET `/api/admin/audit`
**Resumo:** Get Audit Logs
**Tags:** Admin - BI & Metrics

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `limit` | query | ❌ | integer |

---

## GET `/api/admin/audit/financial/reconciliation`
**Resumo:** Get Reconciliation Report
**Tags:** Admin - BI & Metrics

---

## GET `/api/admin/audit/financial/ledger`
**Resumo:** Get Ledger History
**Tags:** Admin - BI & Metrics

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `limit` | query | ❌ | integer |

---

## GET `/api/admin/audit/financial/verify-integrity`
**Resumo:** Verify Ledger Integrity
**Tags:** Admin - BI & Metrics

---

## POST `/api/admin/audit/financial/fix-orphan`
**Resumo:** Fix Orphan Transaction
**Tags:** Admin - BI & Metrics

---

## GET `/api/admin/metrics`
**Resumo:** Get Dashboard Metrics
**Tags:** Admin - BI & Metrics

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `start_date` | query | ❌ | string |
| `end_date` | query | ❌ | string |

---

## GET `/api/admin/marketing/promotions`
**Resumo:** List Promotions
**Tags:** Admin - Marketing

---

## POST `/api/admin/marketing/promotions`
**Resumo:** Create Promotion
**Tags:** Admin - Marketing

---

## PATCH `/api/admin/marketing/promotions/{promo_id}`
**Resumo:** Update Promotion
**Tags:** Admin - Marketing

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `promo_id` | path | ✅ | string |

---

## DELETE `/api/admin/marketing/promotions/{promo_id}`
**Resumo:** Delete Promotion
**Tags:** Admin - Marketing

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `promo_id` | path | ✅ | string |

---

## POST `/api/admin/marketing/recommendations/generate`
**Resumo:** Trigger Recommendation Engine
**Tags:** Admin - Marketing

---

## GET `/api/admin/marketing/whatsapp/status`
**Resumo:** Check Whatsapp Status
**Tags:** Admin - Marketing

---

## POST `/api/admin/marketing/whatsapp/test`
**Resumo:** Test Whatsapp Connection
**Tags:** Admin - Marketing

---

## GET `/api/admin/franchise/dashboard`
**Resumo:** Get Franchise Dashboard
**Tags:** Admin - Franchise

---

## GET `/api/admin/integrations/webhooks`
**Resumo:** List Webhooks
**Tags:** Admin - Integrations & Webhooks

---

## POST `/api/admin/integrations/webhooks`
**Resumo:** Create Webhook
**Tags:** Admin - Integrations & Webhooks

---

## DELETE `/api/admin/integrations/webhooks/{webhook_id}`
**Resumo:** Delete Webhook
**Tags:** Admin - Integrations & Webhooks

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `webhook_id` | path | ✅ | integer |

---

## GET `/api/admin/company/me`
**Resumo:** Get My Company
**Tags:** SaaS - Billing & Settings

---

## PATCH `/api/admin/company/me`
**Resumo:** Update My Company
**Tags:** SaaS - Billing & Settings

---

## PATCH `/api/admin/company/me/password`
**Resumo:** Update Password
**Tags:** SaaS - Billing & Settings

---

## POST `/api/admin/billing/upgrade`
**Resumo:** Upgrade To Pro
**Tags:** SaaS - Billing & Settings

---

## POST `/api/admin/billing/portal`
**Resumo:** Manage Billing
**Tags:** SaaS - Billing & Settings

---

## GET `/api/admin/payment/auth-url/{provider}`
**Resumo:** Get Auth Url
**Tags:** SaaS - Billing & Settings

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `provider` | path | ✅ | string |

---

## POST `/api/admin/payment/callback/{provider}`
**Resumo:** Oauth Callback
**Tags:** SaaS - Billing & Settings

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `provider` | path | ✅ | string |
| `code` | query | ✅ | string |

---

## DELETE `/api/admin/payment/disconnect`
**Resumo:** Disconnect Payment
**Tags:** SaaS - Billing & Settings

---

## POST `/api/admin/fiscal/orders/{order_id}/emit`
**Resumo:** Emit Fiscal Document
**Tags:** SaaS - Fiscal

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `order_id` | path | ✅ | string |

---

## GET `/api/admin/financial/tips`
**Resumo:** Get Tips Report
**Tags:** SaaS - Financial Reports

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `start_date` | query | ❌ | string |
| `end_date` | query | ❌ | string |

---

## GET `/api/admin/ai/forecast`
**Resumo:** Get Sales Forecast
**Tags:** Admin - Intelligence

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `days` | query | ❌ | integer |

---

## GET `/api/admin/{company_slug}/history`
**Resumo:** Get Order History
**Tags:** Admin - History

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `company_slug` | path | ✅ | string |
| `page` | query | ❌ | integer |
| `limit` | query | ❌ | integer |
| `status` | query | ❌ | any |
| `start_date` | query | ❌ | any |
| `end_date` | query | ❌ | any |

---

## POST `/api/webhooks/mercadopago`
**Resumo:** Mercadopago Webhook
**Tags:** Inbound Webhooks

---

## POST `/api/webhooks/stripe`
**Resumo:** Stripe Webhook
**Tags:** Inbound Webhooks

### Parâmetros
| Nome | Local | Obrigatório | Tipo |
| :--- | :--- | :---: | :--- |
| `stripe-signature` | header | ❌ | string |

---

## POST `/api/webhooks/fiscal/focus`
**Resumo:** Focus Nfe Webhook
**Tags:** Inbound Webhooks

---

## POST `/api/webhooks`
**Resumo:** Ifood Webhook
**Tags:** Inbound Webhooks

---

## POST `/api/payments/process`
**Resumo:** Process Payment
**Tags:** Inbound Webhooks

---

