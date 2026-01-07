# 🛡️ Auditoria Técnica: Contrato JWT Backend

**Data:** 2026-01-07
**Status:** HOMOLOGADO
**Referência:** `app/routers/auth.py` | `app/core/security.py`

## 1. Evidência de Payload (Access Token)
O backend MesaFlow emite tokens compatíveis com o padrão OpenID Connect, contendo as claims necessárias para o endurecimento semântico do mobile.

**Estrutura de Claims validada:**
```json
{
  "sub": "admin@mesaflow.com",      // Identificador único (Email)
  "role": "owner",                  // RBAC (owner, manager, cashier, kitchen, driver)
  "account_type": "company",        // Contexto de conta
  "company_id": "uuid-v4-string",   // Tenant ID (Obrigatório para staff)
  "iat": 1736123456,                // Issued At
  "exp": 1736125256                 // expiration (30 min padrão)
}
```

## 2. Fluxo de Renovação (Refresh)
- **Endpoint:** `POST /api/auth/refresh`
- **Requisito:** Header `X-Refresh-Token`.
- **Comportamento:** O backend invalida semanticamente o par antigo e emite um par novo.
- **Fail-Safe:** Qualquer inconsistência retorna `401 Unauthorized`, gatilho para o `logout()` atômico no Mobile.

## 3. Conclusão da Auditoria
O contrato atual do backend suporta integralmente a **Missão 14A** e permite que o **AuthGate** tome decisões soberanas de renderização sem necessidade de chamadas extras ao `/me` nesta fase.
