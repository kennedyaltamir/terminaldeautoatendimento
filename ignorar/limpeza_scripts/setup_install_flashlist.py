import subprocess
import os
import sys

def install_flashlist():
    print("🚀 Instalando @shopify/flash-list (TASK-041)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    try:
        # Instalação via Expo para garantir compatibilidade nativa
        print("📦 Executando: npx expo install @shopify/flash-list")
        subprocess.check_call("npx expo install @shopify/flash-list", cwd=mobile_dir, shell=True)
        
        print("✅ FlashList instalado com sucesso.")
        print("⚠️  IMPORTANTE: Como é uma biblioteca nativa, você precisará gerar um novo Prebuild ou APK.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Falha na instalação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_flashlist()
