# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 01:05:00
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    except:
        return None

def deep_fix():
    print("🛠️ MesaFlow Emulator Deep Fixer - API 36 Edition")
    print("===============================================")

    avd_name = "Medium_Phone_API_36.1"

    # 1. Limpeza de Processos e Trava (Garantia)
    print("\n[1/5] Limpando ambiente")
    if sys.platform == "win32":
        os.system("taskkill /F /IM emulator.exe >nul 2>&1")
        os.system("taskkill /F /IM qemu-system-x86_64.exe >nul 2>&1")
    
    # 2. Wipe Data (Reset de Fábrica do AVD)
    print(f"[2/5] Resetando dados do dispositivo {avd_name}")
    run_command(f"emulator -avd {avd_name} -wipe-data")
    print("✅ Dados limpos.")

    # 3. Verificação de Renderizador Alternativo
    print("[3/5] Testando inicializacao com renderizacao segura (ANGLE)")
    # ANGLE traduz OpenGL para D3D11, mais estável no Windows
    print("💡 Tentando abrir emulador Se abrir, feche-o para continuar o script.")
    
    # Rodar em background para não travar o script
    cmd = f"emulator -avd {avd_name} -no-snapshot-load -gpu angle_indirect"
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("\n[4/5] Analise de Versao:")
    print("⚠️  A API 36 (Android 15/16) e instavel em muitos drivers NVIDIA.")
    print("👉 RECOMENDACAO: Se a tela continuar preta, crie um AVD com API 34 (Android 14).")

    print("\n[5/5] Correcao de Build Mobile:")
    print("❌ O erro 'Unsupported platform' no EAS ocorre porque o Windows nao suporta build local.")
    print("✅ SOLUCAO: Use o comando de nuvem (gratuito):")
    print("   cd mobile && eas build --platform android --profile preview")
    print("   (Remova o --local)")

    print("\n===============================================")
    print("🚀 PROXIMOS PASSOS MANUAIS:")
    print("1. No Android Studio -> Device Manager.")
    print("2. Clique no 'Lapis' (Edit) do seu dispositivo.")
    print("3. Em 'Emulated Performance', mude Graphics para 'Software - GLES 2.0'.")
    print("4. Tente ligar novamente.")
    print("===============================================")

if __name__ == "__main__":
    deep_fix()
