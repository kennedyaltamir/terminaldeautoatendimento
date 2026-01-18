
@echo off
SETLOCAL EnableDelayedExpansion

echo ==========================================
echo 🚀 MESAFLOW MOBILE LAUNCHER (WINDOWS)
echo ==========================================

:: 1. Executar Auditoria
echo [1/4] Executando Auditoria de Ambiente...
python scripts/maintenance/mobile_build_audit.py
if !errorlevel! neq 0 goto ErrorAudit

:: 2. Entrar no diretório
cd mobile
if !errorlevel! neq 0 (
    echo ❌ Erro: Pasta 'mobile' nao encontrada.
    goto End
)

:: 3. Instalar dependências se necessário
if exist "node_modules" goto SkipInstall

echo [2/4] Instalando dependencias (npm install)...
call npm install
if !errorlevel! neq 0 goto ErrorInstall
goto NextStep

:SkipInstall
echo [2/4] Dependencias ja instaladas.

:NextStep
:: 4. Limpar Cache
echo [3/4] Limpando cache do Metro Bundler...
del /q %TEMP%\metro-cache 2>nul

:: 5. Iniciar Expo
echo [4/4] Iniciando Expo (Android)...
echo.
echo ⚠️  Certifique-se que o Emulador Android esta aberto ou um dispositivo USB conectado.
echo.
call npx expo start --android --clear
goto End

:ErrorAudit
echo.
echo ❌ Falha na auditoria. Corrija os erros acima e tente novamente.
pause
goto End

:ErrorInstall
echo.
echo ❌ Falha na instalacao de dependencias.
pause
goto End

:End
ENDLOCAL

