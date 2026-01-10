# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:55:00
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), -1

def diagnose():
    print("🔍 MesaFlow Emulator Diagnostician v1.0")
    print("========================================")

    # 1. Verificar ADB e Dispositivos
    print("\n[1/5] Verificando conexao ADB")
    out, code = run_command("adb devices")
    if code == 0:
        print(f"Status: OK\n{out}")
    else:
        print("❌ Erro: ADB nao encontrado ou falhou.")

    # 2. Verificar AVDs instalados
    print("\n[2/5] Listando Dispositivos Virtuais (AVDs)")
    out, code = run_command("emulator -list-avds")
    avds = out.split('\n') if out else []
    if avds:
        print(f"Encontrados: {', '.join(avds)}")
        target_avd = avds[0]
    else:
        print("❌ Erro: Nenhum AVD encontrado. Crie um no Android Studio.")
        return

    # 3. Verificar Espaco em Disco
    print("\n[3/5] Verificando recursos do sistema")
    import shutil
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    print(f"Espaco livre em disco: {free_gb}GB")
    if free_gb < 5:
        print("⚠️  Aviso: Menos de 5GB livres. O emulador pode falhar.")

    # 4. Testar Cold Boot (Solucao para Possibilidade 2)
    print("\n[4/5] Sugestao de Correcao: COLD BOOT")
    print(f"Se a tela continua preta, tente rodar manualmente:")
    print(f"   emulator -avd {target_avd} -no-snapshot-load")

    # 5. Testar Renderizacao de Software (Solucao para Possibilidade 1)
    print("\n[5/5] Sugestao de Correcao: SOFTWARE RENDERING")
    print(f"Se houver erro de GPU, tente rodar:")
    print(f"   emulator -avd {target_avd} -gpu swiftshader_indirect")

    print("\n========================================")
    print("🚀 ACOES RECOMENDADAS AGORA:")
    print(f"1. Feche o Android Studio completamente.")
    print(f"2. No terminal, execute o comando de limpeza de cache:")
    print(f"   emulator -avd {target_avd} -wipe-data")
    print(f"3. Inicie com Cold Boot:")
    print(f"   emulator -avd {target_avd} -no-snapshot-load")
    print("========================================")

if __name__ == "__main__":
    diagnose()
