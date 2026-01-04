import subprocess
import os
import sys

def install_deps():
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("❌ Pasta 'frontend' não encontrada.")
        return

    print("📦 Instalando dependências de UI (Framer Motion)...")
    
    # Framer Motion é usado para as transições suaves no Login/Registro
    cmd = ["npm", "install", "framer-motion"]
    
    try:
        subprocess.check_call(cmd, cwd=frontend_dir, shell=True)
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar: {e}")

if __name__ == "__main__":
    install_deps()