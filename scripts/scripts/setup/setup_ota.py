import subprocess
import os
import sys

def setup_ota():
    print("🚀 Configurando OTA Updates (Expo Updates)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    try:
        # Instala o pacote expo-updates
        print("📦 Instalando expo-updates...")
        subprocess.check_call("npx expo install expo-updates", cwd=mobile_dir, shell=True)
        
        print("✅ Pacote instalado com sucesso.")
        print("ℹ️  Nota: As configurações de 'updates' e 'runtimeVersion' já foram aplicadas no app.json.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Falha na instalação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_ota()
