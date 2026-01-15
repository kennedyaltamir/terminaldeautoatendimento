# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 15:15:00
import os
import subprocess
import sys

def stabilize():
    print("🔧 Estabilizando Infraestrutura MesaFlow...")
    if sys.platform == "win32":
        try:
            # Mata processos que ocupam a porta do Redis
            output = subprocess.check_output("netstat -ano | findstr :6379", shell=True).decode()
            for line in output.splitlines():
                if "LISTENING" in line:
                    pid = line.strip().split()[-1]
                    print(f"   [!] Encerrando processo zumbi {pid}...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True)
        except: pass

    print("🐳 Reiniciando Docker Redis...")
    subprocess.run("docker rm -f mesaflow-redis", shell=True, capture_output=True)
    subprocess.run("docker run -d -p 6379:6379 --name mesaflow-redis redis:alpine", shell=True, check=True)
    print("✅ Redis operacional.")

if __name__ == "__main__":
    stabilize()
