import subprocess
import os
import time
from datetime import datetime

# [TEST_EXEMPT: Script de automação de hardware/emulador]

OUTPUT_DIR = "docs/screenshots/mobile"
PACKAGE_NAME = "com.mesaflow.mobile"

def run_adb(command):
    try:
        result = subprocess.run(f"adb {command}", shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Erro ADB: {e}")
        return ""

def capture_screen(name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    local_path = os.path.join(OUTPUT_DIR, filename)
    
    print(f"📸 Capturando: {name}...")
    run_adb(f"shell screencap -p /sdcard/{filename}")
    run_adb(f"pull /sdcard/{filename} {local_path}")
    run_adb(f"shell rm /sdcard/{filename}")
    print(f"✅ Salvo em: {local_path}")

def main():
    print("🚀 Iniciando Automação de Screenshots Mobile...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Verificar dispositivo
    device = run_adb("get-state")
    if device != "device":
        print("❌ Nenhum dispositivo ou emulador detectado via ADB.")
        return

    # 2. Fluxo de Captura (Manual assistido)
    screens = [
        "01_Login_Screen",
        "02_KDS_Dashboard",
        "03_Order_Detail",
        "04_Settings_SilentMode"
    ]

    print("\nInstruções:")
    print("Navegue manualmente no emulador até a tela desejada e pressione ENTER para capturar.")
    
    for screen in screens:
        input(f"👉 Vá para a tela: {screen} e pressione ENTER...")
        capture_screen(screen)

    print("\n✨ Processo concluído. Verifique a pasta docs/screenshots/mobile")

if __name__ == "__main__":
    main()
