@echo off
echo ==========================================
echo 📦 MESAFLOW DELIVERY E2E RUNNER
echo ==========================================
echo.

:: 1. Seed de Dados (Garante estado limpo)
echo [1/2] Semeando banco de dados...
python scripts/maintenance/seed_logistics.py
if %errorlevel% neq 0 (
    echo ❌ Falha no Seed. Verifique o backend.
    exit /b 1
)

:: 2. Executar Teste Playwright
echo.
echo [2/2] Executando testes E2E...
cd frontend
call npx playwright test tests/delivery_e2e.spec.ts --project=chromium --headed
if %errorlevel% neq 0 (
    echo ❌ Testes falharam.
    exit /b 1
)

echo.
echo ✅ SUITE DE ENTREGA CONCLUIDA COM SUCESSO.
pause