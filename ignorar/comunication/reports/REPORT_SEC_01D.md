# 🧪 Passive Read-Only Probe Report (SEC-01D)

## Objetivo
Provar a filtragem estrutural do RLS via análise de plano de execução (EXPLAIN).

**Role Utilizada:** mesaflow_app (RESTRICTED)

## Plano de Execução Analisado
```sql
Index Scan using idx_orders_company_created on public.orders
  Output: id, company_id, table_id, session_id, driver_id, promotion_id, order_type, origin, external_order_id, customer_phone, delivery_address, delivery_code, subtotal, discount_amount, cashback_earned, service_fee, delivery_fee, status, payment_method, payment_status, mp_payment_id, mp_qr_code, mp_qr_code_base64, fiscal_status, fiscal_reference_id, nfe_key, nfe_url_xml, nfe_url_pdf, customer_name, total_amount, device_fingerprint, created_at, finished_at
  Index Cond: (orders.company_id = (NULLIF(current_setting('app.current_company_id'::text, true), ''::text))::uuid)
Query Identifier: 6726907439413016745
```

## Veredito Técnico
✅ **PASS:** O motor PostgreSQL injetou corretamente o filtro de segurança no plano de execução.
