import subprocess
import os
import sys

def upgrade_rntl():
    print("🚑 Atualizando React Native Testing Library para v13 (Compatibilidade RN 0.76)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    try:
        # O erro "Unexpected token export" dentro de detectHostComponentNames é um sintoma conhecido
        # de incompatibilidade entre RNTL antigo e React Native 0.76+ (New Architecture).
        # A versão 13.x do RNTL corrige a detecção de componentes nativos.
        
        print("📦 Instalando @testing-library/react-native@^13.0.0...")
        cmd = "npm install @testing-library/react-native@^13.0.0 --save-dev --legacy-peer-deps"
        subprocess.check_call(cmd, cwd=mobile_dir, shell=True)

        print("✅ RNTL Atualizado.")
        
        # Limpeza de cache é vital após troca de versão de lib de teste
        print("🧹 Limpando cache do Jest...")
        subprocess.run("npx jest --clearCache", cwd=mobile_dir, shell=True, check=False)

    except subprocess.CalledProcessError as e:
        print(f"❌ Falha na execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    upgrade_rntl()
