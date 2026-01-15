@echo off
echo ==========================================
echo 🚚 MESAFLOW DELIVERY E2E RUNNER
echo ==========================================
echo.
echo [1/2] Preparando ambiente de teste...
cd frontend

echo [2/2] Executando suite de logistica (Chromium)...
npx playwright test tests/delivery_e2e.spec.ts --project=chromium --headed

if %errorlevel% neq 0 (
    echo.
    echo ❌ FALHA NOS TESTES. Verifique o relatorio.
    exit /b 1
)

echo.
echo ✅ SUCESSO: Fluxo de entrega validado.
pause
