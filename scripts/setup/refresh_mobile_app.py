import os
import subprocess
import glob
from pathlib import Path

# [TEST_EXEMPT: Script de utilidade para automação de ambiente local]

def run_command(cmd):
    try:
        # shell=True é necessário para comandos com caminhos complexos no Windows
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def refresh_app():
    print("🚀 Iniciando atualização automática do App no Emulador...")

    adb_path = r"C:\Users\Kennedy Oliveira\AppData\Local\Android\Sdk\platform-tools\adb.exe"
    package_name = "com.mesaflow.mobile"
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    # 1. Localizar o APK mais recente
    list_of_files = glob.glob(os.path.join(downloads_path, "application-*.apk"))
    if not list_of_files:
        print("❌ Nenhum APK encontrado na pasta Downloads.")
        print(f"   Procurei em: {downloads_path}")
        return

    latest_apk = max(list_of_files, key=os.path.getctime)
    print(f"📦 APK detectado: {os.path.basename(latest_apk)}")

    # 2. Verificar se o emulador está online
    devices = run_command(f'"{adb_path}" devices')
    if "emulator" not in devices:
        print("⚠️  AVISO: Nenhum emulador detectado. Ligue o Android Studio primeiro.")
        return

    # 3. Desinstalar versão antiga
    print("🧹 Removendo versão antiga...")
    run_command(f'"{adb_path}" uninstall {package_name}')

    # 4. Instalar nova versão
    print("🚀 Instalando nova versão...")
    install_res = run_command(f'"{adb_path}" install "{latest_apk}"')
    
    if "Success" in install_res:
        print("✨ Sucesso! O aplicativo foi atualizado.")
    else:
        print(f"❌ Falha na instalação: {install_res}")

if __name__ == "__main__":
    refresh_app()
