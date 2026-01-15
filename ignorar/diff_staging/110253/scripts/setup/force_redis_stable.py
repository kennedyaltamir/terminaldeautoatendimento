# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:15:00
import os
import subprocess
import sys

def kill_redis_zombies():
    print("💀 Procurando processos Redis zumbis na porta 6379...")
    if sys.platform == "win32":
        try:
            # Encontra o PID usando a porta 6379
            output = subprocess.check_output("netstat -ano | findstr :6379", shell=True).decode()
            for line in output.splitlines():
                if "LISTENING" in line:
                    pid = line.strip().split()[-1]
                    print(f"   [!] Matando processo {pid}...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True)
        except:
            print("   ✅ Nenhuma trava de porta detectada.")

def restart_docker_redis():
    print("🐳 Reiniciando container Docker...")
    subprocess.run("docker rm -f mesaflow-redis", shell=True, capture_output=True)
    subprocess.run("docker run -d -p 6379:6379 --name mesaflow-redis redis:alpine", shell=True, check=True)
    print("✅ Redis reiniciado.")

if __name__ == "__main__":
    kill_redis_zombies()
    restart_docker_redis()
