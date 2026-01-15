import subprocess
import os
import sys

def fix_renderer():
    print("🚑 Executando Protocolo de Correção de Renderer (React 18)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    try:
        # 1. Remover o pacote problemático
        print("🗑️  1. Removendo react-test-renderer (versão fantasma)...")
        subprocess.run("npm remove react-test-renderer", cwd=mobile_dir, shell=True, check=False)

        # 2. Instalar a versão correta (18.3.1)
        print("📦 2. Instalando react-test-renderer@18.3.1...")
        subprocess.check_call("npm install react-test-renderer@18.3.1 --save-dev --legacy-peer-deps", cwd=mobile_dir, shell=True)

        # 3. Fixar testing-library compatível
        print("🔧 3. Fixando @testing-library/react-native@12.9.0...")
        subprocess.check_call("npm install @testing-library/react-native@12.9.0 --save-dev --legacy-peer-deps", cwd=mobile_dir, shell=True)

        # 4. Alinhar Jest e Expo
        print("🧪 4. Alinhando Jest e Expo...")
        cmd_align = (
            "npm install "
            "jest@29.7.0 "
            "jest-expo@52.0.6 "
            "babel-preset-expo@12.0.0 "
            "--save-dev --legacy-peer-deps"
        )
        subprocess.check_call(cmd_align, cwd=mobile_dir, shell=True)

        print("✅ Ambiente de Testes Mobile corrigido.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Falha na execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_renderer()
