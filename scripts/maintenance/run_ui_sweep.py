
import os
import time
import subprocess
import re
import sys

# Configuração
APP_FILE = "mobile/App.tsx"
TIMEOUT_SECONDS = 120 # Tempo total para varrer todas as telas
EXPECTED_SCREENS = 11 # Total de telas no array

def modify_app_mode(enable_sweep: bool):
    """Ativa ou desativa o modo UI Sweep no App.tsx"""
    print(f"🔧 {'Ativando' if enable_sweep else 'Desativando'} modo UI Sweep...")
    
    with open(APP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if enable_sweep:
        new_content = content.replace("const IS_UI_SWEEP_MODE = false;", "const IS_UI_SWEEP_MODE = true;")
    else:
        new_content = content.replace("const IS_UI_SWEEP_MODE = true;", "const IS_UI_SWEEP_MODE = false;")
    
    with open(APP_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

def monitor_sweep():
    print("🕵️  Monitorando Varredura Visual (ADB)...")
    
    # Limpa logs antigos
    subprocess.run("adb logcat -c", shell=True)
    
    process = subprocess.Popen(
        ["adb", "logcat", "-v", "time", "*:S", "ReactNative:V", "ReactNativeJS:V"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',
        errors='replace'
    )

    success_count = 0
    start_time = time.time()
    
    try:
        while True:
            line = process.stdout.readline()
            if not line: continue
            
            # Detecta início
            if "[UI_SWEEP] INITIATING SEQUENCE" in line:
                print("🚀 Sequência de teste iniciada no dispositivo.")

            # Detecta sucesso individual
            if "[UI_SWEEP] RESULT:" in line:
                screen = line.split("RESULT:")[1].strip()
                print(f"   ✅ {screen}")
                success_count += 1

            # Detecta falha
            if "[UI_SWEEP] FAILURE:" in line:
                print(f"   ❌ {line.strip()}")
                return False

            # Detecta fim
            if "[UI_SWEEP] SEQUENCE COMPLETED" in line:
                print(f"\n✨ Varredura concluída. Telas validadas: {success_count}/{EXPECTED_SCREENS}")
                return success_count >= EXPECTED_SCREENS

            # Timeout
            if time.time() - start_time > TIMEOUT_SECONDS:
                print("\n⏱️  Timeout aguardando conclusão do teste.")
                return False

    except KeyboardInterrupt:
        return False
    finally:
        process.kill()

def main():
    print("========================================")
    print("🛡️  MESAFLOW AUTOMATED UI SWEEP (L5)")
    print("========================================")
    
    try:
        # 1. Ativar Modo Sweep
        modify_app_mode(True)
        
        print("⏳ Aguardando recarga do Metro Bundler (Pressione 'r' no terminal do Metro se necessário)...")
        print("   (Você tem 10 segundos para garantir que o app recarregou)")
        time.sleep(5) 
        
        # 2. Monitorar
        success = monitor_sweep()
        
        # 3. Reverter Modo (Sempre)
        modify_app_mode(False)
        
        if success:
            print("\n✅ SUCESSO: Todas as telas renderizam corretamente.")
            sys.exit(0)
        else:
            print("\n❌ FALHA: Alguma tela quebrou ou o teste não completou.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        modify_app_mode(False) # Garantia de rollback
        sys.exit(1)

if __name__ == "__main__":
    main()

