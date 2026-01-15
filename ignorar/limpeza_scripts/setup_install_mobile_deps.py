import subprocess
import os
import sys

def install_mobile_dependencies():
    print("📦 Instalando dependências do Mobile (npm install --legacy-peer-deps)...")
    
    current_dir = os.getcwd()
    
    # Detecta se já está na pasta mobile ou na raiz
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")
    
    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    try:
        # --legacy-peer-deps é necessário devido ao conflito entre React 19 e libs nativas
        subprocess.check_call("npm install --legacy-peer-deps", cwd=mobile_dir, shell=True)
        print("✅ Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Falha ao instalar dependências: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_mobile_dependencies()