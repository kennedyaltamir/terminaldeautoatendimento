# Database Schema Discovery Report

## Overview
This report represents the **single source of truth** of the current database schema.

## Tables Analysis

### Table: `alembic_version`
**Columns:**
- `version_num` : character varying
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `audit_logs`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `user_name` : character varying
- `user_role` : character varying
- `action` : character varying
- `resource` : character varying
- `resource_id` : character varying
- `details` : json
- `ip_address` : character varying
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `categories`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `name` : character varying
- `order_index` : integer
- `availability_days` : json
- `start_time` : time without time zone
- `end_time` : time without time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `companies`
**Columns:**
- `id` : uuid
- `name` : character varying
- `slug` : character varying
- `custom_domain` : character varying
- `owner_email` : character varying
- `owner_phone` : character varying
- `owner_role` : character varying
- `password_hash` : character varying
- `plan_tier` : character varying
- `segment` : character varying
- `trial_ends_at` : timestamp with time zone
- `is_active` : boolean
- `is_email_verified` : boolean
- `stripe_customer_id` : character varying
- `stripe_subscription_id` : character varying
- `subscription_status` : character varying
- `logo_url` : character varying
- `banner_url` : character varying
- `primary_color` : character varying
- `background_color` : character varying
- `text_color` : character varying
- `accent_color` : character varying
- `instagram_url` : character varying
- `whatsapp_number` : character varying
- `whatsapp_api_url` : character varying
- `whatsapp_instance` : character varying
- `whatsapp_token` : character varying
- `ifood_merchant_id` : character varying
- `ifood_token` : text
- `wifi_ssid` : character varying
- `wifi_password` : character varying
- `payment_provider` : character varying
- `payment_credentials` : json
- `pix_key` : character varying
- `mp_access_token` : character varying
- `mp_user_id` : character varying
- `marketplace_fee_percentage` : numeric
- `pending_commission_balance` : numeric
- `loyalty_percentage` : numeric
- `service_fee_percentage` : numeric
- `fixed_delivery_fee` : numeric
- `cnpj` : character varying
- `inscricao_estadual` : character varying
- `fiscal_token` : character varying
- `csc_token` : character varying
- `csc_id` : character varying
- `opens_at` : time without time zone
- `closes_at` : time without time zone
- `created_at` : timestamp with time zone
- Has `company_id`: **False**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `customer_wallets`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `customer_phone` : character varying
- `balance` : numeric
- `updated_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `driver_ledger`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `driver_id` : integer
- `order_id` : uuid
- `type` : character varying
- `amount` : numeric
- `description` : character varying
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `employees`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `name` : character varying
- `email` : character varying
- `password_hash` : character varying
- `role` : character varying
- `is_active` : boolean
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `feature_flags`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `key` : character varying
- `is_enabled` : boolean
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `financial_ledger`
**Columns:**
- `id` : uuid
- `sequence_id` : bigint
- `company_id` : uuid
- `entry_type` : character varying
- `amount` : bigint
- `balance_after` : bigint
- `category` : character varying
- `description` : character varying
- `reference_id` : character varying
- `integrity_hash` : character varying
- `metadata_json` : json
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `ingredients`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `supplier_id` : integer
- `name` : character varying
- `unit` : character varying
- `current_stock` : numeric
- `min_stock_alert` : numeric
- `cost_per_unit` : numeric
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `leads`
**Columns:**
- `id` : integer
- `email` : character varying
- `source` : character varying
- `created_at` : timestamp with time zone
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `option_groups`
**Columns:**
- `id` : integer
- `product_id` : integer
- `name` : character varying
- `min_selection` : integer
- `max_selection` : integer
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `options`
**Columns:**
- `id` : integer
- `group_id` : integer
- `name` : character varying
- `price` : numeric
- `is_available` : boolean
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `order_feedbacks`
**Columns:**
- `id` : integer
- `order_id` : uuid
- `company_id` : uuid
- `score` : integer
- `comment` : text
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `order_item_options`
**Columns:**
- `id` : integer
- `order_item_id` : integer
- `option_id` : integer
- `name` : character varying
- `price` : numeric
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `order_items`
**Columns:**
- `id` : integer
- `order_id` : uuid
- `product_id` : integer
- `quantity` : integer
- `unit_price` : numeric
- `notes` : text
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `orders`
**Columns:**
- `id` : uuid
- `company_id` : uuid
- `table_id` : integer
- `session_id` : integer
- `driver_id` : integer
- `promotion_id` : uuid
- `order_type` : character varying
- `origin` : character varying
- `external_order_id` : character varying
- `customer_phone` : character varying
- `delivery_address` : text
- `delivery_code` : character varying
- `subtotal` : numeric
- `discount_amount` : numeric
- `cashback_earned` : numeric
- `service_fee` : numeric
- `delivery_fee` : numeric
- `status` : character varying
- `payment_method` : character varying
- `payment_status` : character varying
- `mp_payment_id` : character varying
- `mp_qr_code` : text
- `mp_qr_code_base64` : text
- `fiscal_status` : character varying
- `fiscal_reference_id` : character varying
- `nfe_key` : character varying
- `nfe_url_xml` : character varying
- `nfe_url_pdf` : character varying
- `customer_name` : character varying
- `total_amount` : numeric
- `device_fingerprint` : character varying
- `created_at` : timestamp with time zone
- `finished_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `password_reset_tokens`
**Columns:**
- `id` : integer
- `user_email` : character varying
- `token` : character varying
- `expires_at` : timestamp with time zone
- `used` : boolean
- `created_at` : timestamp with time zone
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `payment_transactions`
**Columns:**
- `id` : uuid
- `company_id` : uuid
- `order_id` : uuid
- `provider` : character varying
- `external_id` : character varying
- `status` : character varying
- `amount` : numeric
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `product_recipes`
**Columns:**
- `id` : integer
- `product_id` : integer
- `ingredient_id` : integer
- `quantity_required` : numeric
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `product_recommendations`
**Columns:**
- `source_product_id` : integer
- `target_product_id` : integer
- Has `company_id`: **False**
- RLS Enabled: **False**
- Policies: **NONE**

### Table: `products`
**Columns:**
- `id` : integer
- `category_id` : integer
- `name` : character varying
- `description` : text
- `price` : numeric
- `image_url` : character varying
- `is_available` : boolean
- `short_code` : character varying
- `track_stock` : boolean
- `stock_quantity` : integer
- `station` : character varying
- `tags` : json
- `ncm` : character varying
- `cfop` : character varying
- `external_id` : character varying
- Has `company_id`: **False**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `promotions`
**Columns:**
- `id` : uuid
- `company_id` : uuid
- `name` : character varying
- `code` : character varying
- `discount_type` : character varying
- `discount_value` : numeric
- `min_order_value` : numeric
- `max_discount_value` : numeric
- `start_date` : timestamp with time zone
- `end_date` : timestamp with time zone
- `usage_limit` : integer
- `current_usage` : integer
- `is_active` : boolean
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `service_fee_ledger`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `employee_id` : integer
- `order_id` : uuid
- `amount` : numeric
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `service_requests`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `table_id` : integer
- `service_type` : character varying
- `notes` : text
- `status` : character varying
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `suppliers`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `name` : character varying
- `contact_name` : character varying
- `phone` : character varying
- `email` : character varying
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `table_sessions`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `table_id` : integer
- `opened_by_employee_id` : integer
- `customer_name` : character varying
- `customer_phone` : character varying
- `session_token` : character varying
- `access_pin` : character varying
- `is_active` : boolean
- `created_at` : timestamp with time zone
- `closed_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `tables`
**Columns:**
- `table_catalog` : name
- `id` : integer
- `table_schema` : name
- `company_id` : uuid
- `table_name` : name
- `table_number` : integer
- `qr_token` : character varying
- `table_type` : character varying
- `self_referencing_column_name` : name
- `is_active` : boolean
- `reference_generation` : character varying
- `position_x` : numeric
- `user_defined_type_catalog` : name
- `position_y` : numeric
- `user_defined_type_schema` : name
- `user_defined_type_name` : name
- `is_insertable_into` : character varying
- `is_typed` : character varying
- `commit_action` : character varying
- Has `company_id`: **True**
- RLS Enabled: **False**
- Policies:
  - `tenant_isolation_policy`

### Table: `user_devices`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `employee_id` : integer
- `fcm_token` : character varying
- `platform` : character varying
- `device_name` : character varying
- `updated_at` : timestamp with time zone
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

### Table: `webhook_subscriptions`
**Columns:**
- `id` : integer
- `company_id` : uuid
- `target_url` : character varying
- `events` : json
- `secret` : character varying
- `is_active` : boolean
- `created_at` : timestamp with time zone
- Has `company_id`: **True**
- RLS Enabled: **True**
- Policies:
  - `tenant_isolation_policy`

## Conclusion
This schema snapshot must be used for all subsequent migrations and security enforcement.