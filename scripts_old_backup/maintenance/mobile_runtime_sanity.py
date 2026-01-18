
import subprocess
import time
import sys
import re

# Configuração
TIMEOUT_SECONDS = 60
EXPECTED_LOGS = [
    r"\[MESAFLOW_SANITY\] App Mounting",
    r"\[MESAFLOW_SANITY\] Navigation Container Ready",
    r"\[MESAFLOW_SANITY\] Hydration Complete"
]

def run_adb_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return ""

def monitor_logs():
    print("🕵️  Iniciando Monitoramento de Sanidade Mobile (ADB)...")
    print("    Aguardando sinais vitais do aplicativo...")
    
    # Limpa o buffer de log antigo
    run_adb_command("adb logcat -c")
    
    start_time = time.time()
    found_logs = set()
    
    # Processo de leitura de logs
    process = subprocess.Popen(
        ["adb", "logcat", "-v", "time", "*:S", "ReactNative:V", "ReactNativeJS:V"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',
        errors='replace'
    )

    try:
        while True:
            line = process.stdout.readline()
            if not line:
                continue
                
            # Verifica padrões esperados
            for pattern in EXPECTED_LOGS:
                if re.search(pattern, line) and pattern not in found_logs:
                    print(f"   ✅ Sinal Detectado: {pattern.replace(r'[MESAFLOW_SANITY] ', '')}")
                    found_logs.add(pattern)
            
            # Verifica erros críticos
            if "FATAL EXCEPTION" in line or "RedBox" in line:
                print(f"\n❌ CRASH DETECTADO:\n{line.strip()}")
                return False

            # Condição de Sucesso
            if len(found_logs) == len(EXPECTED_LOGS):
                print("\n✨ TODOS OS SINAIS VITAIS CONFIRMADOS!")
                return True

            # Timeout
            if time.time() - start_time > TIMEOUT_SECONDS:
                print("\n⏱️  Timeout aguardando inicialização do app.")
                missing = [p for p in EXPECTED_LOGS if p not in found_logs]
                print(f"   Sinais ausentes: {missing}")
                return False

    except KeyboardInterrupt:
        print("\n🛑 Monitoramento interrompido.")
        return False
    finally:
        process.kill()

if __name__ == "__main__":
    if monitor_logs():
        sys.exit(0)
    else:
        sys.exit(1)

