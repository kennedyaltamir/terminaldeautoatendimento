
@echo off
echo ==========================================
echo 🚀 MESAFLOW PRODUCTION LAUNCHER
echo ==========================================
echo.

:: 1. Verificações Finais
echo [1/3] Verificando integridade...
python comunication/scripts/gov_04_registry_drift.py
if %errorlevel% neq 0 (
    echo ❌ FALHA DE INTEGRIDADE DETECTADA. ABORTANDO.
    pause
    exit /b 1
)

:: 2. Healthcheck
echo [2/3] Testando conexao...
python comunication/scripts/inf_01_healthcheck.py
if %errorlevel% neq 0 (
    echo ⚠️  AVISO: O servidor parece estar offline ou inacessivel.
    echo    Tentando iniciar mesmo assim...
)

:: 3. Iniciar
echo [3/3] Iniciando Sistema...
echo.
echo    - Backend: http://localhost:8000
echo    - Frontend: http://localhost:3000
echo.
echo Pressione CTRL+C para parar.
echo.

python run.py

