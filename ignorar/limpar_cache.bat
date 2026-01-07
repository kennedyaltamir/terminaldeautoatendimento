@echo off
echo 🧹 Limpando caches Python (__pycache__)...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo 🗑️ Removendo arquivos temporarios...
del /s /q *.pyc

echo ✅ Limpeza concluida!
pause