# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 03:00:00
import os
import subprocess
import time
from pathlib import Path

# Configurações
OUTPUT_DIR = Path("docs/screenshots/mobile")
SCHEME = "mesaflow"

# Mapeamento de Telas e suas URIs de Deep Link
SCREENS = [
    {"name": "01_Login", "uri": f"{SCHEME}://login"},
    {"name": "02_Waiter_Dashboard", "uri": f"{SCHEME}://waiter"},
    {"name": "03_Kitchen_Dashboard", "uri": f"{SCHEME}://kitchen"},
    {"name": "04_Driver_Dashboard", "uri": f"{SCHEME}://driver"},
]

def run_adb(command):
    try:
        # Executa comando ADB e captura saída
        result = subprocess.run(f"adb {command}", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, result.stderr
        return result.stdout.strip(), None
    except Exception as e:
        return None, str(e)

def capture():
    print("📱 MesaFlow Mobile Visual Auditor v1.0")
    print("========================================")

    # 1. Preparar diretório
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True)
        print(f"📁 Pasta criada: {OUTPUT_DIR}")

    # 2. Verificar se há dispositivos conectados
    devices, err = run_adb("devices")
    if not devices or "emulator-" not in devices:
        print("❌ ERRO: Nenhum emulador Android detectado.")
        print("Certifique-se de que o Android Studio esta com o AVD ligado.")
        return

    print("✅ Emulador detectado. Iniciando sequencia de captura")

    for screen in SCREENS:
        name = screen["name"]
        uri = screen["uri"]
        
        print(f"🚀 Navegando para: {name} ({uri})")
        
        # Dispara o Deep Link via ADB
        # am start -W (wait for launch)
        run_adb(f"shell am start -a android.intent.action.VIEW -d {uri}")
        
        # Aguarda renderização (ajuste se o PC for lento)
        time.sleep(3)

        # Tira o print no dispositivo
        device_path = f"/sdcard/{name}.png"
        run_adb(f"shell screencap -p {device_path}")

        # Traz o arquivo para o computador
        local_path = OUTPUT_DIR / f"{name}.png"
        run_adb(f"pull {device_path} \"{local_path}\"")
        
        # Limpa o arquivo temporario no Android
        run_adb(f"shell rm {device_path}")
        
        print(f"   📸 Captura salva: {local_path.name}")

    print("\n========================================")
    print(f"✨ Auditoria concluida! {len(SCREENS)} telas capturadas.")
    print(f"Local: {OUTPUT_DIR.absolute()}")

if __name__ == "__main__":
    capture()
