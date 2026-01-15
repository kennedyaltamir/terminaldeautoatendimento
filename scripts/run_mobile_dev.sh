
#!/bin/bash

echo "=========================================="
echo "🚀 MESAFLOW MOBILE LAUNCHER (UNIX)"
echo "=========================================="

# 1. Executar Auditoria
echo "[1/4] Executando Auditoria de Ambiente..."
python3 scripts/maintenance/mobile_build_audit.py
if [ $? -ne 0 ]; then
    echo "❌ Falha na auditoria. Abortando."
    exit 1
fi

# 2. Entrar no diretório
cd mobile

# 3. Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "[2/4] Instalando dependências (npm install)..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Falha no npm install."
        exit 1
    fi
else
    echo "[2/4] Dependências já instaladas."
fi

# 4. Iniciar Expo
echo "[3/4] Iniciando Expo..."
npx expo start --clear

