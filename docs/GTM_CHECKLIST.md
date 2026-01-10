# 🚀 MesaFlow Go-To-Market (GTM) Readiness Checklist

**Date:** 2026-01-08
**Target:** Production Launch
**Status:** DRAFT

This document outlines the critical gaps identified for the 2026 GTM launch based on the current repository state.

## 1. Infrastructure & Resilience (Critical)
- [ ] **Database Pooling:** Verify `app/database.py` enforces `pool_pre_ping=True` and optimal pool sizes.
- [ ] **Connection String:** Ensure production documentation explicitly requires Neon pooled connection string (`-pooler`).
- [ ] **Web Server:** Validate `render.yaml` configures Gunicorn workers correctly for concurrency.
- [ ] **Reference Task:** `TASK-GTM-01`

## 2. Observability & Monitoring
- [ ] **Sentry Backend:** Confirm `sentry_sdk` captures `company_id` in context.
- [ ] **Sentry Frontend:** Verify `@sentry/nextjs` integration and source maps upload.
- [ ] **Structured Logs:** Ensure backend logs are emitted in JSON format for production ingestion.
- [ ] **Reference Task:** `TASK-GTM-02`

## 3. Mobile & Distribution
- [ ] **Build Configuration:** Validate `mobile/eas.json` has a `production` profile generating `.aab` (Android) and `.ipa` (iOS).
- [ ] **Metadata:** Check `mobile/app.json` for correct versioning, icons, and splash screens.
- [ ] **Permissions:** Audit `android.permissions` to remove unnecessary requests.
- [ ] **Reference Task:** `TASK-GTM-03`

## 4. Compliance & Legal
- [ ] **Public Routes:** Verify existence of `/terms` and `/privacy` pages in Next.js.
- [ ] **Content:** Ensure content matches `docs/legal/TERMS_OF_SERVICE.md` and `PRIVACY_POLICY.md`.
- [ ] **Footer:** Check for links and CNPJ display in the public footer.
- [ ] **Reference Task:** `TASK-GTM-04`

## 5. Fintech Integrity
- [ ] **Centavos Refactor:** Confirm migration from Float to Integer (Cents) for all monetary values.
- [ ] **Split Logic:** Validate marketplace fee calculations in `PaymentService`.
- [ ] **Reference Task:** `TASK-FIN-01`

## 6. Security Hardening
- [ ] **RLS:** Confirm Row-Level Security is active on all core tables.
- [ ] **Webhook Signatures:** Verify HMAC validation for iFood, Stripe, and Mercado Pago.
- [ ] **Reference Task:** `TASK-SEC-01`