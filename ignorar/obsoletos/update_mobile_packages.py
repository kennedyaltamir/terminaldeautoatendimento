import subprocess
import os
import sys

def update_packages():
    print("🚀 Iniciando atualização segura de pacotes Mobile...")
    
    mobile_dir = os.path.join(os.getcwd(), "mobile")
    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    try:
        # 1. Instala ferramenta de atualização se não existir
        print("📦 Verificando npm-check-updates...")
        subprocess.run("npm list -g npm-check-updates", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 2. Atualiza package.json (Interativo/Seguro)
        # Ignora react e react-native para manter compatibilidade com Expo SDK 54
        print("🔄 Atualizando versões no package.json (exceto core)...")
        cmd_update = "npx npm-check-updates -u --reject react,react-native,expo"
        subprocess.check_call(cmd_update, cwd=mobile_dir, shell=True)

        # 3. Instalação
        print("📦 Instalando novas versões...")
        subprocess.check_call("npm install --legacy-peer-deps", cwd=mobile_dir, shell=True)
        
        # 4. Correção de alinhamento Expo
        print("🔧 Alinhando versões do Expo SDK 54...")
        subprocess.check_call("npx expo install --fix", cwd=mobile_dir, shell=True)

        print("✅ Atualização concluída com sucesso.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante a atualização: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_packages()
