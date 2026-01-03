import subprocess
import sys
import importlib.util

def check_and_install(package, install_name=None):
    if install_name is None:
        install_name = package
        
    spec = importlib.util.find_spec(package)
    if spec is None:
        print(f"📦 Instalando {install_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
            print(f"✅ {install_name} instalado com sucesso!")
        except subprocess.CalledProcessError:
            print(f"❌ Falha ao instalar {install_name}.")
            sys.exit(1)
    else:
        print(f"✅ {install_name} já está instalado.")

if __name__ == "__main__":
    print("🔧 Verificando dependências críticas para a Task 2 (Redis)...")
    
    # Instala o cliente Redis para Python
    check_and_install("redis")
    
    print("\n🎉 Dependências corrigidas! Agora você pode rodar os testes.")