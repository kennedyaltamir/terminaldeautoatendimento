@echo off
echo 🗑️  Limpando caches e node_modules...

cd frontend
if exist node_modules (
    rmdir /s /q node_modules
    echo ✅ node_modules removido
)
if exist .next (
    rmdir /s /q .next
    echo ✅ .next cache removido
)
if exist package-lock.json (
    del package-lock.json
    echo ✅ lockfile removido
)

echo 📦 Reinstalando dependencias limpas...
call npm install

echo 🚀 Pronto! Execute 'python run.py' novamente.
pause