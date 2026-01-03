import subprocess
import sys
import importlib.util

def check_and_install(package):
    spec = importlib.util.find_spec(package)
    if spec is None:
        print(f"📦 Instalando {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} instalado com sucesso!")
        except subprocess.CalledProcessError:
            print(f"❌ Falha ao instalar {package}.")
            sys.exit(1)
    else:
        print(f"✅ {package} já está instalado.")

if __name__ == "__main__":
    print("🔧 Configurando ambiente de testes assíncronos...")
    check_and_install("pytest-asyncio")
    print("\n🎉 Ambiente pronto!")