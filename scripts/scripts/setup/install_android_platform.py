import os
import subprocess
import sys
from pathlib import Path

def find_sdk_manager(sdk_path):
    """Tenta localizar o binário sdkmanager em locais padrão."""
    possible_paths = [
        sdk_path / "cmdline-tools" / "latest" / "bin" / "sdkmanager.bat",
        sdk_path / "cmdline-tools" / "bin" / "sdkmanager.bat",
        sdk_path / "tools" / "bin" / "sdkmanager.bat",
    ]
    
    for p in possible_paths:
        if p.exists():
            return p
    return None

def install_platform():
    print("🔧 Verificando componentes do Android SDK (NDK & CMake)...")

    # 1. Ler o local.properties para achar o SDK
    root_dir = Path.cwd()
    local_props = root_dir / "mobile" / "android" / "local.properties"
    
    if not local_props.exists():
        print("❌ Arquivo local.properties não encontrado. Rode o fix_android_sdk.py primeiro.")
        return

    sdk_dir = None
    with open(local_props, "r") as f:
        for line in f:
            if line.startswith("sdk.dir"):
                path_str = line.split("=")[1].strip()
                # Corrige barras escapadas se necessário
                path_str = path_str.replace("\\:", ":").replace("\\\\", "\\")
                sdk_dir = Path(path_str)
                break
    
    if not sdk_dir or not sdk_dir.exists():
        print(f"❌ Diretório do SDK inválido: {sdk_dir}")
        return

    print(f"📂 SDK detectado em: {sdk_dir}")

    # 2. Localizar sdkmanager
    sdkmanager = find_sdk_manager(sdk_dir)
    if not sdkmanager:
        print("⚠️  'sdkmanager' não encontrado via script.")
        print("   👉 Solução Manual: Abra o Android Studio > SDK Manager > SDK Tools.")
        print("   👉 Marque 'Show Package Details' e instale:")
        print("      - NDK (Side by side) -> 26.1.10909125")
        print("      - CMake -> 3.22.1")
        return

    # 3. Instalar Componentes Críticos para Expo 54 / RN 0.76
    packages = [
        "platforms;android-34",
        "build-tools;34.0.0",
        "platform-tools",
        "ndk;26.1.10909125", # Obrigatório para RN 0.76+
        "cmake;3.22.1"       # Obrigatório para Hermes/Expo Modules
    ]
    
    print(f"⬇️  Instalando pacotes: {', '.join(packages)}...")
    print("   (Isso pode demorar alguns minutos dependendo da internet)")

    # O comando "echo y |" serve para aceitar as licenças automaticamente
    cmd = f'echo y | "{str(sdkmanager)}" --install ' + " ".join([f'"{p}"' for p in packages])
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("\n✅ Componentes instalados com sucesso!")
        print("   - NDK 26.1 configurado")
        print("   - CMake 3.22 configurado")
        print("🚀 Tente rodar o build novamente.")
    except subprocess.CalledProcessError:
        print("\n❌ Falha ao instalar via linha de comando.")
        print("👉 Por favor, abra o Android Studio e instale o NDK 26.1 e CMake 3.22.1 manualmente.")

if __name__ == "__main__":
    install_platform()
