import os
import subprocess
import sys
import re
from pathlib import Path

def find_microsoft_jdk():
    """Localiza o Microsoft OpenJDK 17."""
    print("🔍 Procurando Microsoft OpenJDK 17...")
    
    base_path = Path(r"C:\Program Files\Microsoft")
    if not base_path.exists():
        print(f"❌ Pasta {base_path} não encontrada.")
        return None

    # Procura pastas que começam com jdk-17
    for item in base_path.iterdir():
        if item.is_dir() and item.name.startswith("jdk-17"):
            java_home = item
            print(f"✅ JDK Encontrado: {java_home}")
            return java_home
            
    print("❌ JDK 17 da Microsoft não encontrado na pasta padrão.")
    return None

def fix_gradle_ndk(ndk_version="26.1.10909125"):
    """Garante que o build.gradle use a versão exata do NDK instalada."""
    print(f"🔧 Configurando NDK {ndk_version} no build.gradle...")
    
    gradle_file = Path.cwd() / "mobile" / "android" / "build.gradle"
    
    if not gradle_file.exists():
        print("❌ build.gradle não encontrado.")
        return

    try:
        with open(gradle_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Substitui qualquer ndkVersion existente pela correta
        if "ndkVersion" in content:
            new_content = re.sub(
                r'ndkVersion\s*=\s*".*"', 
                f'ndkVersion = "{ndk_version}"', 
                content
            )
        else:
            # Se não existir, injeta no bloco ext
            new_content = content.replace(
                "ext {", 
                f'ext {{\n        ndkVersion = "{ndk_version}"', 
                1
            )

        with open(gradle_file, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print("✅ Versão do NDK fixada no Gradle.")
        
    except Exception as e:
        print(f"❌ Erro ao editar Gradle: {e}")

def run_build(java_home):
    print("\n🚀 Iniciando Build com Java 17...")
    
    # Configura variáveis de ambiente para este processo
    env = os.environ.copy()
    env["JAVA_HOME"] = str(java_home)
    env["PATH"] = f"{java_home}\\bin;" + env["PATH"]
    
    android_dir = Path.cwd() / "mobile" / "android"
    gradlew = "gradlew.bat"
    
    # 1. Clean
    print("🧹 Limpando cache (Clean)...")
    subprocess.run([str(android_dir / gradlew), "clean"], cwd=android_dir, env=env, shell=True)
    
    # 2. Build
    print("📦 Compilando APK (AssembleRelease)...")
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
            os.startfile(apk_path.parent)
        else:
            print("\n⚠️ Build finalizado, mas APK não encontrado.")
            
    except subprocess.CalledProcessError:
        print("\n❌ Falha no Build. Verifique os logs acima.")

if __name__ == "__main__":
    jdk_path = find_microsoft_jdk()
    if jdk_path:
        # Usa o NDK 26 que instalamos anteriormente via script
        fix_gradle_ndk("26.1.10909125")
        run_build(jdk_path)
    else:
        print("\n👉 Instale o Microsoft OpenJDK 17 e tente novamente.")
