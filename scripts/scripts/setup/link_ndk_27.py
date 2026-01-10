import os
import sys
import subprocess
import re
from pathlib import Path

# Configuração Alvo
TARGET_NDK_VERSION = "27.1.12297006"

def find_jdk17():
    """Localiza o Microsoft OpenJDK 17 ou similar."""
    print("🔍 Procurando JDK 17...")
    base_path = Path(r"C:\Program Files\Microsoft")
    if base_path.exists():
        for item in base_path.iterdir():
            if item.is_dir() and item.name.startswith("jdk-17"):
                return item
    
    # Fallback para JAVA_HOME se estiver definido
    env_home = os.environ.get("JAVA_HOME")
    if env_home and "17" in env_home:
        return Path(env_home)
        
    return None

def get_sdk_path():
    """Localiza o SDK do Android."""
    # Tenta ler do local.properties atual
    root_dir = Path.cwd()
    local_props = root_dir / "mobile" / "android" / "local.properties"
    
    if local_props.exists():
        with open(local_props, "r") as f:
            for line in f:
                if line.strip().startswith("sdk.dir"):
                    path_str = line.split("=")[1].strip()
                    path_str = path_str.replace("\\:", ":").replace("\\\\", "\\")
                    return Path(path_str)
    
    # Fallback padrão Windows
    return Path(os.environ["LOCALAPPDATA"]) / "Android" / "Sdk"

def update_local_properties(sdk_path, ndk_path):
    """Reescreve o local.properties com os caminhos corretos."""
    print(f"🔧 Atualizando local.properties...")
    
    props_file = Path.cwd() / "mobile" / "android" / "local.properties"
    
    # Formato seguro para Windows (escapando barras e dois pontos)
    sdk_str = str(sdk_path).replace("\\", "\\\\").replace(":", "\\:")
    ndk_str = str(ndk_path).replace("\\", "\\\\").replace(":", "\\:")
    
    content = f"sdk.dir={sdk_str}\nndk.dir={ndk_str}\n"
    
    try:
        with open(props_file, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Erro ao escrever local.properties: {e}")
        return False

def update_build_gradle():
    """Força a versão do NDK no app/build.gradle."""
    print(f"🔧 Configurando NDK {TARGET_NDK_VERSION} no app/build.gradle...")
    
    gradle_file = Path.cwd() / "mobile" / "android" / "app" / "build.gradle"
    
    if not gradle_file.exists():
        print("❌ app/build.gradle não encontrado.")
        return False

    try:
        with open(gradle_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Substitui ou insere ndkVersion
        if "ndkVersion" in content:
            new_content = re.sub(
                r'ndkVersion\s+["\'].*["\']', 
                f'ndkVersion "{TARGET_NDK_VERSION}"', 
                content
            )
        else:
            new_content = re.sub(
                r'android\s*\{', 
                f'android {{\n    ndkVersion "{TARGET_NDK_VERSION}"', 
                content,
                count=1
            )

        with open(gradle_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao editar Gradle: {e}")
        return False

def run_build(java_home):
    print("\n🚀 Iniciando Build Blindado (NDK 27 + Java 17)...")
    
    android_dir = Path.cwd() / "mobile" / "android"
    gradlew = "gradlew.bat" if os.name == "nt" else "./gradlew"
    
    # Configura ambiente
    env = os.environ.copy()
    env["JAVA_HOME"] = str(java_home)
    env["PATH"] = f"{java_home}\\bin;" + env["PATH"]
    
    # 1. Clean
    print("🧹 Limpando cache...")
    subprocess.run([str(android_dir / gradlew), "clean"], cwd=android_dir, env=env, shell=True)
    
    # 2. Build
    print("📦 Compilando APK...")
    try:
        subprocess.run(
            [str(android_dir / gradlew), "assembleRelease"], 
            cwd=android_dir, 
            env=env, 
            check=True, 
            shell=True
        )
        
        apk_path = android_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        if apk_path.exists():
            print(f"\n🏆 SUCESSO! APK gerado em:\n{apk_path}")
            if os.name == "nt":
                os.startfile(apk_path.parent)
        else:
            print("\n⚠️ Build finalizado, mas APK não encontrado.")

    except subprocess.CalledProcessError:
        print("\n❌ Falha no Build.")

def main():
    print(f"🔍 Verificando instalação do NDK {TARGET_NDK_VERSION}...")
    
    # 1. Validar SDK e NDK
    sdk_path = get_sdk_path()
    ndk_path = sdk_path / "ndk" / TARGET_NDK_VERSION
    
    if not ndk_path.exists():
        print(f"❌ NDK {TARGET_NDK_VERSION} não encontrado em {ndk_path}")
        return

    print(f"✅ NDK encontrado.")

    # 2. Validar Java
    jdk_path = find_jdk17()
    if not jdk_path:
        print("❌ JDK 17 não encontrado.")
        return
    
    print(f"✅ JDK 17 encontrado: {jdk_path}")

    # 3. Aplicar Configurações
    if update_local_properties(sdk_path, ndk_path) and update_build_gradle():
        # 4. Executar Build
        run_build(jdk_path)

if __name__ == "__main__":
    main()
