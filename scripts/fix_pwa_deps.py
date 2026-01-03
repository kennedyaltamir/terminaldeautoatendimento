import subprocess
import os
import sys

def install_pwa():
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("❌ Pasta 'frontend' não encontrada.")
        return

    print("📦 Instalando plugin PWA e atualizando dependências...")
    
    # Instala especificamente o pacote que faltava
    cmd = ["npm", "install"]
    
    try:
        subprocess.check_call(cmd, cwd=frontend_dir, shell=True)
        print("✅ Dependências corrigidas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar: {e}")

if __name__ == "__main__":
    install_pwa()