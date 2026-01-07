@echo off
echo 💀 Matando TODOS os processos Python e Node...
taskkill /F /IM python.exe /T
taskkill /F /IM uvicorn.exe /T
taskkill /F /IM node.exe /T

echo 🧹 Limpando arquivos compilados (Cache)...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc

echo ✅ Ambiente limpo. Pode rodar o 'run.py' agora.
pause