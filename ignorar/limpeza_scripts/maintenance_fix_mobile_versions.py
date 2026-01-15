import subprocess
import os
import sys

def fix_mobile_env():
    print("🚑 Executando Protocolo de Correção de Versões (React 18 / Jest 29)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    try:
        # 1. Downgrade do Core (React & Jest)
        # Removemos React 19 e Jest 30 que causam o conflito e o erro de sintaxe
        # Voltamos o testing-library para a versão 12 que é estável com React 18
        print("📦 1. Restaurando Core (React 18.3.1, Jest 29.7.0)...")
        cmd_core = (
            "npm install "
            "react@18.3.1 "
            "react-dom@18.3.1 "
            "@types/react@~18.3.12 "
            "jest@^29.7.0 "
            "@testing-library/react-native@^12.9.0 "
            "--legacy-peer-deps"
        )
        subprocess.check_call(cmd_core, cwd=mobile_dir, shell=True)

        # 2. Alinhamento do Expo
        # O --fix vai garantir que jest-expo e babel-preset-expo batam com a versão do 'expo' instalada
        print("🔧 2. Alinhando dependências nativas (Expo Fix)...")
        subprocess.check_call("npx expo install --fix", cwd=mobile_dir, shell=True)

        print("✅ Ambiente Mobile restaurado para padrões do Expo.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Falha na execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_mobile_env()
