import os
import subprocess
import sys
from pathlib import Path

def main():
    print("🔧 Preparando ambiente de Build Blindado...")

    # 1. Configurar caminhos
    root_dir = Path.cwd()
    android_dir = root_dir / "mobile" / "android"
    
    # Caminho exato do NDK 26 (baseado nos seus logs de erro anteriores)
    # O Gradle estava pegando o 27 automaticamente, vamos forçar o 26
    ndk_26_path = Path(r"C:\Users\Kennedy Oliveira\AppData\Local\Android\Sdk\ndk\26.1.10909125")
    
    if not ndk_26_path.exists():
        print(f"❌ ERRO CRÍTICO: NDK 26 não encontrado em: {ndk_26_path}")
        print("   Execute: python scripts/setup/install_android_platform.py")
        return

    print(f"✅ NDK 26 detectado: {ndk_26_path}")

    # 2. Preparar Variáveis de Ambiente (Isso sobrescreve a detecção automática do Gradle)
    env = os.environ.copy()
    env["ANDROID_NDK_HOME"] = str(ndk_26_path)
    env["NDK_HOME"] = str(ndk_26_path)
    
    # Garante JAVA_HOME (se não estiver setado, tenta achar)
    if "JAVA_HOME" not in env:
        # Tenta achar o JDK 17 padrão do VS Code/Android Studio
        possible_java = Path(r"C:\Program Files\Microsoft\jdk-17.0.17.10-hotspot")
        if possible_java.exists():
            env["JAVA_HOME"] = str(possible_java)
            print(f"✅ JAVA_HOME forçado: {possible_java}")

    # 3. Definir comando Gradle (Windows vs Unix)
    gradlew = "gradlew.bat" if os.name == "nt" else "./gradlew"
    gradle_path = android_dir / gradlew

    if not gradle_path.exists():
        print("❌ 'gradlew' não encontrado. O projeto nativo foi gerado?")
        return

    # 4. Executar CLEAN (Crucial para remover o cache do NDK 27)
    print("\n🧹 Executando Gradle Clean (Limpando caches)...")
    try:
        subprocess.run(
            [str(gradle_path), "clean"], 
            cwd=android_dir, 
            env=env, 
            check=True, 
            shell=True
        )
        print("✅ Limpeza concluída.")
    except subprocess.CalledProcessError:
        print("⚠️  Aviso: 'clean' falhou. Tentando prosseguir com o build...")

    # 5. Executar BUILD
    print("\n🚀 Iniciando Compilação do APK (Release)...")
    try:
        # Usamos shell=True no Windows para evitar problemas de permissão com .bat
        process = subprocess.run(
            [str(gradle_path), "assembleRelease"], 
            cwd=android_dir, 
            env=env, 
            check=True, 
            shell=True
        )
        
        # 6. Verificar Resultado
        apk_path = android_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        
        if apk_path.exists():
            print(f"\n🏆 SUCESSO ABSOLUTO! APK gerado em:")
            print(f"   {apk_path}")
            
            # Abre a pasta no Windows
            if os.name == "nt":
                os.startfile(apk_path.parent)
        else:
            print("\n❌ O comando terminou sem erro, mas o APK não foi encontrado.")

    except subprocess.CalledProcessError:
        print("\n❌ FALHA NO BUILD.")
        print("   O erro persiste. Verifique se o NDK 26 está íntegro.")

if __name__ == "__main__":
    main()
