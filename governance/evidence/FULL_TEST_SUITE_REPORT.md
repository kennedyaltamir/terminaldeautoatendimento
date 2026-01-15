# 🛡️ Relatório de Execução de Testes L6
**Data:** 2026-01-15T11:21:11.379712

## 📊 Sumário
| Teste | Status | Duração |
| :--- | :---: | :--- |
| Backend (Lógica/Segurança) | ✅ PASS | 6.10s |
| Frontend (Fluxo UI) | ❌ FAIL | 348.36s |

## 🚩 Detalhes de Falhas
### ❌ Frontend (Fluxo UI)
#### STDERR
```text

```
#### STDOUT
```text

Running 3 tests using 1 worker

[1A[2K[1/3] [setup] › tests\auth.setup.ts:11:6 › authenticate admin
[1A[2K[2/3] [chromium] › tests\logistics_ui.spec.ts:11:5 › Test 9: Driver Transitions to Map
[1A[2K  1) [chromium] › tests\logistics_ui.spec.ts:11:5 › Test 9: Driver Transitions to Map ──────────────

    Error: [2mexpect([22m[31mlocator[39m[2m).[22mtoBeVisible[2m([22m[2m)[22m failed

    Locator: getByTestId('driver.delivery.order.card').first()
    Expected: visible
    Timeout: 15000ms
    Error: element(s) not found

    Call log:
    [2m  - Expect "toBeVisible" with timeout 15000ms[22m
    [2m  - waiting for getByTestId('driver.delivery.order.card').first()[22m


      20 |         // 3. Localiza o card de pedido disponível
      21 |         const card = page.getByTestId('driver.delivery.order.card').first();
    > 22 |         await expect(card).toBeVisible({ 
         |                            ^
      23 |             timeout: 15000,
      24 |             message: "ERRO: Nenhum pedido disponível. Execute 'python scripts/maintenance/seed_ui_states.py' antes do teste."
      25 |         });
        at C:\mesaflow\frontend\tests\logistics_ui.spec.ts:22:28

    attachment #1: screenshot (image/png) ──────────────────────────────────────────────────────────
    test-results\logistics_ui-Test-9-Driver-Transitions-to-Map-chromium\test-failed-1.png
    ────────────────────────────────────────────────────────────────────────────────────────────────

    Error Context: test-results\logistics_ui-Test-9-Driver-Transitions-to-Map-chromium\error-context.md


[1A[2K[3/3] [chromium] › tests\logistics_ui.spec.ts:41:5 › Test 10: Client Passive Tracking
[1A[2K  1 failed
    [chromium] › tests\logistics_ui.spec.ts:11:5 › Test 9: Driver Transitions to Map ───────────────
  1 did not run
  1 passed (24.0s)

[36m  Serving HTML report at http://localhost:9323. Press Ctrl+C to quit.[39m

```
 