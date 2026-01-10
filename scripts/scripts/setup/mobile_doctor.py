import os
import sys
import shutil
import subprocess
import re
from pathlib import Path

def find_jdk17():
    """Procura pelo JDK 17 em locais padrão do Windows."""
    print("🔍 Procurando instalação do JDK 17...")
    
    program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    search_paths = [
        Path(program_files) / "Microsoft",
        Path(program_files) / "Java",
        Path(program_files) / "Eclipse Adoptium",
        Path(program_files) / "Zulu",
    ]

    for base_path in search_paths:
        if base_path.exists():
            for folder in base_path.iterdir():
                if "jdk-17" in folder.name.lower() or "jdk17" in folder.name.lower():
                    java_bin = folder / "bin" / "java.exe"
                    if java_bin.exists():
                        return folder
    return None

def check_and_fix_java():
    print("☕ Verificando versão do Java...")
    
    # Tenta rodar java -version
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        output = result.stderr
        match = re.search(r'version "(\d+)', output)
        if not match: match = re.search(r'version "1\.(\d+)', output)
        
        current_version = int(match.group(1)) if match else 0
        print(f"   Versão atual no PATH: JDK {current_version}")

        if current_version == 17:
            return True
            
    except FileNotFoundError:
        print("   Java não detectado no PATH.")

    # Se não for 17, tenta achar e forçar
    print("⚠️  Versão incorreta. Tentando localizar JDK 17 instalado...")
    jdk17_path = find_jdk17()
    
    if jdk17_path:
        print(f"✅ JDK 17 encontrado em: {jdk17_path}")
        print("   Forçando variáveis de ambiente para este processo...")
        
        # Atualiza as variáveis APENAS para este script e subprocessos
        os.environ["JAVA_HOME"] = str(jdk17_path)
        os.environ["PATH"] = f"{jdk17_path}\\bin;" + os.environ["PATH"]
        return True
    else:
        print("\n❌ ERRO CRÍTICO: JDK 17 não encontrado no sistema.")
        print("   Certifique-se de ter instalado o 'Microsoft Build of OpenJDK 17'.")
        return False

def hard_reset_android():
    print("\n🧹 Realizando Hard Reset na pasta Android...")
    root_dir = Path.cwd()
    mobile_dir = root_dir / "mobile"
    android_dir = mobile_dir / "android"

    if android_dir.exists():
        print("   Removendo pasta 'android' antiga...")
        try:
            # Comando robusto para deletar no Windows
            subprocess.run(f'rmdir /s /q "{android_dir}"', shell=True)
        except Exception as e:
            print(f"⚠️  Erro ao apagar: {e}")

    print("   Gerando novo projeto nativo (Prebuild)...")
    try:
        # Usa npx.cmd no Windows
        npx = "npx.cmd" if os.name == "nt" else "npx"
        subprocess.run([npx, "expo", "prebuild", "--platform", "android", "--clean"], cwd=mobile_dir, check=True, shell=True)
        print("✅ Prebuild concluído.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Falha no Prebuild.")
        return False

def run_build():
    print("\n🚀 Iniciando Build Limpo...")
    root_dir = Path.cwd()
    android_dir = root_dir / "mobile" / "android"
    
    gradlew = "gradlew.bat" if os.name == "nt" else "./gradlew"
    gradle_path = android_dir / gradlew

    if not gradle_path.exists():
        print("❌ Gradle wrapper não encontrado.")
        return

    try:
        # Usa as variáveis de ambiente atualizadas (com JAVA 17)
        print("   Limpando cache do Gradle...")
        subprocess.run([str(gradle_path), "clean"], cwd=android_dir, shell=True, check=True)
        
        print("   Compilando APK...")
        subprocess.run([str(gradle_path), "assembleRelease"], cwd=android_dir, shell=True, check=True)
        
        apk_path = android_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        if apk_path.exists():
            print(f"\n✅ SUCESSO! APK gerado em:\n{apk_path}")
            if os.name == "nt":
                os.startfile(apk_path.parent)
        else:
            print("\n❌ Build terminou mas APK não foi encontrado.")
            
    except subprocess.CalledProcessError:
        print("\n❌ Falha no Build Gradle.")

if __name__ == "__main__":
    if check_and_fix_java():
        if hard_reset_android():
            run_build()
