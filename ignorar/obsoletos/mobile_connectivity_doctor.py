import os
import sys
import subprocess
import urllib.request
import time
from pathlib import Path

def check_backend_status():
    print("1️⃣  Verificando Backend (API)...")
    try:
        # Tenta conectar no health check
        with urllib.request.urlopen("http://localhost:8000/api/health", timeout=2) as response:
            if response.getcode() == 200:
                print("   ✅ Backend está ONLINE e respondendo.")
                return True
    except Exception as e:
        print(f"   ❌ Backend OFFLINE ou inacessível: {e}")
        print("      👉 Certifique-se de rodar 'python run.py' em outro terminal.")
        return False

def check_adb_devices():
    print("\n2️⃣  Verificando Dispositivos Conectados...")
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        output = result.stdout.strip()
        if "device" in output.replace("List of devices attached", "").strip():
            print("   ✅ Dispositivo/Emulador detectado.")
            return True
        else:
            print("   ❌ Nenhum dispositivo encontrado.")
            return False
    except FileNotFoundError:
        print("   ❌ Comando 'adb' não encontrado.")
        return False

def apply_adb_reverse():
    print("\n3️⃣  Aplicando Correção de Roteamento (ADB Reverse)...")
    print("   Isso permite que o Emulador acesse 'localhost:8000' do seu PC.")
    
    try:
        # Mapeia a porta 8000 do Android para a 8000 do PC
        subprocess.run(["adb", "reverse", "tcp:8000", "tcp:8000"], check=True)
        print("   ✅ Roteamento aplicado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ Falha ao aplicar 'adb reverse'.")
        return False

def diagnose_env_file():
    print("\n4️⃣  Analisando Configuração de Build (.env)...")
    env_path = Path("mobile/.env")
    
    if not env_path.exists():
        print("   ⚠️  Arquivo mobile/.env não encontrado.")
        return

    with open(env_path, "r") as f:
        content = f.read()
        print(f"   Conteúdo atual:\n   ---Start---\n{content.strip()}\n   ---End---")
        
        if "localhost" in content:
            print("\n   ℹ️  NOTA: Você está usando 'localhost'.")
            print("       Isso exige que o comando 'adb reverse' (Passo 3) seja rodado sempre que conectar o cabo/emulador.")
        elif "10.0.2.2" in content:
            print("\n   ℹ️  NOTA: Você está usando '10.0.2.2'. Isso funciona nativamente no Emulador Android, mas não no iOS ou Físico.")
        else:
            print("\n   ℹ️  NOTA: Você está usando um IP específico (LAN). Certifique-se que o celular está no mesmo Wi-Fi.")

def main():
    print("🩺 INICIANDO DIAGNÓSTICO DE CONECTIVIDADE MOBILE\n")
    
    backend_ok = check_backend_status()
    device_ok = check_adb_devices()
    
    if device_ok:
        reverse_ok = apply_adb_reverse()
        
        if reverse_ok and backend_ok:
            print("\n🎉 DIAGNÓSTICO CONCLUÍDO: TUDO PARECE CERTO!")
            print("👉 Feche o App no emulador (arraste para cima e feche) e abra novamente.")
            print("👉 Tente fazer login.")
        elif not backend_ok:
            print("\n🛑 O Backend não está rodando. O App não vai conectar sem ele.")
    
    diagnose_env_file()

if __name__ == "__main__":
    main()
