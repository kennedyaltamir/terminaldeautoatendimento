
@echo off
SETLOCAL EnableDelayedExpansion

echo ==========================================
echo 🚀 MESAFLOW MOBILE CI/CD (LOCAL RUNNER)
echo ==========================================

:: 1. UI Sweep (Visual Validation)
echo.
echo [1/5] Executando UI Sweep (L5)...
python scripts/maintenance/run_ui_sweep.py
if !errorlevel! neq 0 goto Error

:: 2. Telemetry Check
echo.
echo [2/5] Verificando Telemetria...
python scripts/maintenance/verify_telemetry.py
if !errorlevel! neq 0 goto Error

:: 3. Production Lock Check
echo.
echo [3/5] Validando Production Lock...
python scripts/maintenance/verify_production_ready.py
if !errorlevel! neq 0 goto Error

:: 4. EAS Readiness
echo.
echo [4/5] Verificando EAS...
python scripts/maintenance/verify_eas_ready.py
if !errorlevel! neq 0 goto Error

:: 5. Build Simulation (Dry Run)
echo.
echo [5/5] Simulando Build (Prebuild)...
cd mobile
call npx expo prebuild --platform android --clean
if !errorlevel! neq 0 goto Error

echo.
echo ✅ CI/CD LOCAL FINALIZADO COM SUCESSO!
echo    O projeto esta pronto para 'eas build --platform android --profile production'.
goto End

:Error
echo.
echo ❌ FALHA NO PIPELINE. CORRIJA OS ERROS ACIMA.
exit /b 1

:End
ENDLOCAL

