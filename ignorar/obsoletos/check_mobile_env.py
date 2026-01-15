import os
import subprocess
import sys

def check_env():
    print("🔍 Verificando ambiente para Build Mobile Local...")
    
    # 1. Verificar JAVA_HOME
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        print(f"✅ JAVA_HOME: {java_home}")
    else:
        print("❌ JAVA_HOME não configurada. Instale o JDK 17 e configure as variáveis de ambiente.")

    # 2. Verificar ANDROID_HOME
    android_home = os.environ.get("ANDROID_HOME")
    if android_home:
        print(f"✅ ANDROID_HOME: {android_home}")
    else:
        print("❌ ANDROID_HOME não configurada. Aponte para a pasta do SDK do Android Studio.")

    # 3. Verificar ADB
    try:
        adb_version = subprocess.check_output(["adb", "version"]).decode()
        print(f"✅ ADB detectado: {adb_version.splitlines()[0]}")
    except:
        print("❌ ADB não encontrado no PATH. Adicione a pasta 'platform-tools' do SDK ao seu PATH.")

    # 4. Verificar Emuladores
    try:
        emulators = subprocess.check_output(["emulator", "-list-avds"]).decode()
        if emulators:
            print(f"✅ Emuladores disponíveis:\n{emulators}")
        else:
            print("⚠️  Nenhum emulador (AVD) criado no Android Studio.")
    except:
        print("❌ Comando 'emulator' não encontrado no PATH.")

if __name__ == "__main__":
    check_env()
