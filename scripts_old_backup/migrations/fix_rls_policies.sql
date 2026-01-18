-- DOMAIN: SECURITY
-- LAST_MODIFIED: 2026-01-13 02:00:00
-- Correção de Policies RLS para garantir isolamento real e tratamento de NULL
-- 1. ORDERS
DROP POLICY IF EXISTS tenant_isolation_policy ON orders;
CREATE POLICY tenant_isolation_policy ON orders
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 2. PRODUCTS
DROP POLICY IF EXISTS tenant_isolation_policy ON products;
CREATE POLICY tenant_isolation_policy ON products
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (category_id IN (SELECT id FROM categories WHERE company_id = current_setting('app.current_company_id', true)::uuid))
    WITH CHECK (category_id IN (SELECT id FROM categories WHERE company_id = current_setting('app.current_company_id', true)::uuid));
-- 3. COMPANIES
DROP POLICY IF EXISTS tenant_isolation_policy ON companies;
CREATE POLICY tenant_isolation_policy ON companies
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (id = current_setting('app.current_company_id', true)::uuid);
-- 4. CUSTOMER_WALLETS
DROP POLICY IF EXISTS tenant_isolation_policy ON customer_wallets;
CREATE POLICY tenant_isolation_policy ON customer_wallets
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 5. DRIVER_LEDGER
DROP POLICY IF EXISTS tenant_isolation_policy ON driver_ledger;
CREATE POLICY tenant_isolation_policy ON driver_ledger
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 6. EMPLOYEES
DROP POLICY IF EXISTS tenant_isolation_policy ON employees;
CREATE POLICY tenant_isolation_policy ON employees
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 7. FINANCIAL_LEDGER
DROP POLICY IF EXISTS tenant_isolation_policy ON financial_ledger;
CREATE POLICY tenant_isolation_policy ON financial_ledger
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 8. INGREDIENTS
DROP POLICY IF EXISTS tenant_isolation_policy ON ingredients;
CREATE POLICY tenant_isolation_policy ON ingredients
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 9. ORDER_FEEDBACKS
DROP POLICY IF EXISTS tenant_isolation_policy ON order_feedbacks;
CREATE POLICY tenant_isolation_policy ON order_feedbacks
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 10. PAYMENT_TRANSACTIONS
DROP POLICY IF EXISTS tenant_isolation_policy ON payment_transactions;
CREATE POLICY tenant_isolation_policy ON payment_transactions
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 11. PROMOTIONS
DROP POLICY IF EXISTS tenant_isolation_policy ON promotions;
CREATE POLICY tenant_isolation_policy ON promotions
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 12. SERVICE_FEE_LEDGER
DROP POLICY IF EXISTS tenant_isolation_policy ON service_fee_ledger;
CREATE POLICY tenant_isolation_policy ON service_fee_ledger
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 13. SERVICE_REQUESTS
DROP POLICY IF EXISTS tenant_isolation_policy ON service_requests;
CREATE POLICY tenant_isolation_policy ON service_requests
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 14. SUPPLIERS
DROP POLICY IF EXISTS tenant_isolation_policy ON suppliers;
CREATE POLICY tenant_isolation_policy ON suppliers
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 15. TABLE_SESSIONS
DROP POLICY IF EXISTS tenant_isolation_policy ON table_sessions;
CREATE POLICY tenant_isolation_policy ON table_sessions
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 16. TABLES
DROP POLICY IF EXISTS tenant_isolation_policy ON tables;
CREATE POLICY tenant_isolation_policy ON tables
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 17. USER_DEVICES
DROP POLICY IF EXISTS tenant_isolation_policy ON user_devices;
CREATE POLICY tenant_isolation_policy ON user_devices
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 18. WEBHOOK_SUBSCRIPTIONS
DROP POLICY IF EXISTS tenant_isolation_policy ON webhook_subscriptions;
CREATE POLICY tenant_isolation_policy ON webhook_subscriptions
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 19. AUDIT_LOGS
DROP POLICY IF EXISTS tenant_isolation_policy ON audit_logs;
CREATE POLICY tenant_isolation_policy ON audit_logs
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 20. CATEGORIES
DROP POLICY IF EXISTS tenant_isolation_policy ON categories;
CREATE POLICY tenant_isolation_policy ON categories
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);
-- 21. FEATURE_FLAGS
DROP POLICY IF EXISTS tenant_isolation_policy ON feature_flags;
CREATE POLICY tenant_isolation_policy ON feature_flags
    AS PERMISSIVE
    FOR ALL
    TO public
    USING (company_id = current_setting('app.current_company_id', true)::uuid)
    WITH CHECK (company_id = current_setting('app.current_company_id', true)::uuid);

