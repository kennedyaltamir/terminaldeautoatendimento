import os
import subprocess
import re
import sys
from pathlib import Path

def find_ndk_17():
    """Localiza a instalação do NDK 17 no sistema."""
    print("🔍 Procurando NDK 17...")
    
    # Caminho padrão do SDK no Windows
    sdk_path = Path(os.environ["LOCALAPPDATA"]) / "Android" / "Sdk"
    ndk_root = sdk_path / "ndk"
    
    if not ndk_root.exists():
        print(f"❌ Pasta NDK não encontrada em: {ndk_root}")
        return None

    # Procura qualquer pasta que comece com "17."
    for folder in ndk_root.iterdir():
        if folder.is_dir() and folder.name.startswith("17."):
            print(f"✅ NDK 17 encontrado: {folder.name}")
            return folder

    print("❌ NDK 17 não encontrado instalado.")
    print("   Versões disponíveis:")
    for folder in ndk_root.iterdir():
        print(f"   - {folder.name}")
    return None

def configure_project(ndk_path):
    """Atualiza os arquivos de configuração do Android."""
    ndk_version = ndk_path.name
    print(f"🔧 Configurando projeto para NDK {ndk_version}...")

    root_dir = Path.cwd()
    
    # 1. Atualizar local.properties
    local_props = root_dir / "mobile" / "android" / "local.properties"
    sdk_path = ndk_path.parent.parent
    
    # Escapar barras para Windows
    ndk_str = str(ndk_path).replace("\\", "\\\\").replace(":", "\\:")
    sdk_str = str(sdk_path).replace("\\", "\\\\").replace(":", "\\:")
    
    with open(local_props, "w", encoding="utf-8") as f:
        f.write(f"sdk.dir={sdk_str}\n")
        f.write(f"ndk.dir={ndk_str}\n")
    print("   -> local.properties atualizado.")

    # 2. Atualizar app/build.gradle
    app_gradle = root_dir / "mobile" / "android" / "app" / "build.gradle"
    
    with open(app_gradle, "r", encoding="utf-8") as f:
        content = f.read()

    # Substitui ou insere ndkVersion
    if "ndkVersion" in content:
        new_content = re.sub(
            r'ndkVersion\s+["\'].*["\']', 
            f'ndkVersion "{ndk_version}"', 
            content
        )
    else:
        new_content = re.sub(
            r'android\s*\{', 
            f'android {{\n    ndkVersion "{ndk_version}"', 
            content,
            count=1
        )

    with open(app_gradle, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("   -> app/build.gradle atualizado.")

def run_build():
    print("\n🚀 Iniciando Build com NDK 17...")
    android_dir = Path.cwd() / "mobile" / "android"
    gradlew = "gradlew.bat" if os.name == "nt" else "./gradlew"
    
    # Limpeza
    print("   Limpando cache...")
    subprocess.run([str(android_dir / gradlew), "clean"], cwd=android_dir, shell=True)
    
    # Build
    print("   Compilando...")
    try:
        subprocess.run(
            [str(android_dir / gradlew), "assembleRelease"], 
            cwd=android_dir, 
            check=True, 
            shell=True
        )
        print("\n🏆 SUCESSO! APK gerado com NDK 17.")
        
        apk_path = android_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        if apk_path.exists() and os.name == "nt":
            os.startfile(apk_path.parent)

    except subprocess.CalledProcessError:
        print("\n❌ Falha no Build.")
        print("   Nota: O React Native 0.76 (Expo 54) pode ser incompatível com NDK 17.")

if __name__ == "__main__":
    ndk_path = find_ndk_17()
    if ndk_path:
        configure_project(ndk_path)
        run_build()
    else:
        print("\n👉 Instale o NDK 17 via Android Studio (SDK Tools > Show Package Details) e tente novamente.")
