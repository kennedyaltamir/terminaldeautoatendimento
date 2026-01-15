@echo off
echo ==================================================
echo 🚀 MESAFLOW DEV ENVIRONMENT LAUNCHER
echo ==================================================
echo.

:: 1. Verificar Python Virtualenv
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtualenv nao encontrado.
    echo    Rode: python -m venv .venv
    echo    Rode: .venv\Scripts\activate
    echo    Rode: pip install -r requirements.txt
    pause
    exit /b
)

:: 2. Iniciar Redis (Docker)
echo [1/3] Verificando Redis...
docker ps | findstr "mesaflow-redis" >nul
if %errorlevel% neq 0 (
    echo    ⚠️  Container Redis nao detectado.
    echo    Tentando iniciar...
    python scripts/setup/smart_redis_setup.py
) else (
    echo    ✅ Redis Online.
)

:: 3. Iniciar Backend (Nova Janela)
echo [2/3] Iniciando Backend (Porta 8000)...
start "MesaFlow Backend" cmd /k "call .venv\Scripts\activate && python run.py"

:: 4. Iniciar Frontend (Nova Janela)
echo [3/3] Iniciando Frontend (Porta 3000)...
start "MesaFlow Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✨ Ambiente iniciado!
echo    Backend: http://localhost:8000/docs
echo    Frontend: http://localhost:3000
echo.
echo Pressione qualquer tecla para fechar este lançador (os terminais permanecerao abertos).
pause >nul
