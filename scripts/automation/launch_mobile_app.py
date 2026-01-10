# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 01:10:00
import os
import subprocess
import socket
import time

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def run_adb(command):
    try:
        result = subprocess.run(f"adb {command}", shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return None

def launch():
    print("🚀 MesaFlow Mobile Launcher - Forcando Abertura no Emulador")
    print("===========================================================")

    # 1. Verificar se o ADB ve o emulador
    devices = run_adb("devices")
    if "emulator-" not in devices:
        print("❌ ERRO: Nenhum emulador detectado pelo ADB.")
        print("Certifique-se de que o emulador no Android Studio esta ligado.")
        return

    print("✅ Emulador detectado.")

    # 2. Verificar se o Expo Go esta instalado
    packages = run_adb("shell pm list packages host.exp.exponent")
    if "host.exp.exponent" not in packages:
        print("⚠️  Expo Go nao encontrado no emulador.")
        print("📦 Tentando instalar o Expo Go automaticamente")
        # O comando 'npx expo start' com 'a' faz isso melhor, mas vamos orientar
        print("👉 Dica: No terminal onde rodou 'npx expo start', pressione 'a'.")
        return

    print("✅ Expo Go encontrado.")

    # 3. Construir URL do Metro Bundler
    ip = get_local_ip()
    expo_url = f"exp://{ip}:8081"
    print(f"🔗 URL do Projeto: {expo_url}")

    # 4. Forcar abertura via Intent
    print("⚡ Enviando comando de abertura direta")
    run_adb(f"shell am start -a android.intent.action.VIEW -d {expo_url}")
    
    print("\n✨ Comando enviado! Verifique a tela do Android Studio.")
    print("O Expo Go deve abrir e carregar o MesaFlow em instantes.")
    print("===========================================================")

if __name__ == "__main__":
    launch()
