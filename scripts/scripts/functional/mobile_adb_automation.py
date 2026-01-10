import subprocess
import time
import os

# [TEST_EXEMPT: Script de automação externa via ADB]

ADB_PATH = r"C:\Users\Kennedy Oliveira\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_adb(command):
    full_cmd = f'"{ADB_PATH}" {command}'
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def test_mobile_flow():
    print("🚀 Iniciando Automação de Teste Nativo via ADB...")

    # 1. Verificar conexão
    devices = run_adb("devices")
    if "device" not in devices.split('\n')[1]:
        print("❌ Erro: Emulador não detectado.")
        return

    # 2. Abrir o Aplicativo
    print("📱 Abrindo MesaFlow...")
    run_adb("shell monkey -p com.mesaflow.mobile -c android.intent.category.LAUNCHER 1")
    time.sleep(5)

    # 3. Simular Digitação de Login (Exemplo de coordenadas para Pixel 8)
    # Nota: As coordenadas variam por tela. Use 'adb shell uiautomator dump' para precisão.
    print("⌨️  Simulando preenchimento de credenciais...")
    run_adb("shell input tap 500 800") # Clica no campo email
    run_adb("shell input text 'admin@mesaflow.com'")
    run_adb("shell input keyevent 66") # Enter
    
    # 4. Capturar Screenshot de Erro/Sucesso
    print("📸 Capturando evidência visual...")
    run_adb("shell screencap -p /sdcard/screen.png")
    run_adb("pull /sdcard/screen.png ./mobile_test_result.png")

    # 5. Verificar Logs Críticos
    print("🔍 Analisando logs de erro (ReactNativeJS)...")
    logs = run_adb("logcat -d ReactNativeJS:E *:S")
    if "Error" in logs:
        print("❌ Erros detectados no log do JavaScript!")
        print(logs)
    else:
        print("✅ Nenhum erro fatal detectado nos logs.")

if __name__ == "__main__":
    test_mobile_flow()
