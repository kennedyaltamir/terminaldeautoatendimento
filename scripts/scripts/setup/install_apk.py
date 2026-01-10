import os
import subprocess
import sys
import shutil
from pathlib import Path

# Tenta ler o package name do app.json para desinstalação correta
PACKAGE_NAME = "com.mesaflow.mobile" 

def find_adb():
    """Tenta localizar o binário ADB no sistema."""
    if shutil.which("adb"):
        return "adb"
    
    root_dir = Path.cwd()
    local_props = root_dir / "mobile" / "android" / "local.properties"
    
    if local_props.exists():
        with open(local_props, "r") as f:
            for line in f:
                if line.startswith("sdk.dir"):
                    sdk_path = line.split("=")[1].strip().replace("\\:", ":").replace("\\\\", "\\")
                    adb_path = Path(sdk_path) / "platform-tools" / "adb.exe"
                    if adb_path.exists():
                        return str(adb_path)
    return None

def install_apk():
    print("📱 Preparando instalação...")
    
    apk_path = Path("mobile/android/app/build/outputs/apk/release/app-release.apk")
    
    if not apk_path.exists():
        print("❌ APK não encontrado.")
        return

    adb = find_adb()
    if not adb:
        print("❌ ADB não encontrado.")
        return

    print(f"🔧 Usando ADB em: {adb}")

    # Verifica dispositivos
    try:
        result = subprocess.run([adb, "devices"], capture_output=True, text=True)
        if "device" not in result.stdout.replace("List of devices attached", "").strip():
            print("⚠️  Nenhum dispositivo conectado.")
            return
    except Exception:
        pass

    print(f"📦 Instalando: {apk_path.name}...")
    
    try:
        # Tenta instalar
        result = subprocess.run([adb, "install", "-r", str(apk_path)], capture_output=True, text=True)
        
        # Verifica sucesso ou erro específico
        if result.returncode == 0:
            print("\n✅ Instalação Concluída com Sucesso!")
            print("   O app 'MesaFlow' deve aparecer no menu do emulador.")
        else:
            # Tratamento de erro de assinatura
            if "INSTALL_FAILED_UPDATE_INCOMPATIBLE" in result.stderr or "INSTALL_FAILED_UPDATE_INCOMPATIBLE" in result.stdout:
                print("\n⚠️  Conflito de assinatura detectado.")
                print(f"   Removendo versão antiga ({PACKAGE_NAME})...")
                
                subprocess.run([adb, "uninstall", PACKAGE_NAME], check=True)
                
                print("   Tentando instalar novamente...")
                subprocess.run([adb, "install", "-r", str(apk_path)], check=True)
                print("\n✅ Instalação Concluída com Sucesso (Após limpeza)!")
            else:
                print(f"\n❌ Erro na instalação:\n{result.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Falha crítica: {e}")

if __name__ == "__main__":
    install_apk()
