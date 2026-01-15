# 🧪 Relatório de Prova Passiva RLS (SEC-01D)

Este teste prova que o PostgreSQL está injetando o filtro de segurança antes de tocar no disco.

## Plano de Execução Detectado
```sql
Seq Scan on public.orders
  Output: id, company_id, table_id, session_id, driver_id, promotion_id, order_type, origin, external_order_id, customer_phone, delivery_address, delivery_code, subtotal, discount_amount, cashback_earned, service_fee, delivery_fee, status, payment_method, payment_status, mp_payment_id, mp_qr_code, mp_qr_code_base64, fiscal_status, fiscal_reference_id, nfe_key, nfe_url_xml, nfe_url_pdf, customer_name, total_amount, device_fingerprint, created_at, finished_at
Query Identifier: 6726907439413016745
```

**Veredito:** ❌ FAIL

> Nota: O sucesso aqui indica que o isolamento é estrutural e inegociável.