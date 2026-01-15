# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:30:00
import os
import subprocess
import sys
import time

def kill_redis_zombies():
    """Procura e encerra processos que travam a porta 6379 no Windows."""
    print("💀 Procurando processos Redis zumbis na porta 6379...")
    if sys.platform == "win32":
        try:
            # Comando para encontrar o PID que escuta na porta 6379
            output = subprocess.check_output("netstat -ano | findstr :6379", shell=True).decode()
            for line in output.splitlines():
                if "LISTENING" in line:
                    parts = line.strip().split()
                    pid = parts[-1]
                    print(f"   [!] Encerrando processo PID {pid}...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
        except Exception:
            print("   ✅ Nenhuma trava de porta detectada.")

def stabilize_infra():
    """Reinicia o container Redis e otimiza o .env para 127.0.0.1."""
    print("🔧 Estabilizando Infraestrutura para Gold Master...")
    
    # 1. Limpa e reinicia container Docker
    print("   [1/2] Reiniciando container Docker 'mesaflow-redis'...")
    subprocess.run("docker rm -f mesaflow-redis", shell=True, capture_output=True)
    try:
        subprocess.run("docker run -d -p 6379:6379 --name mesaflow-redis redis:alpine", shell=True, check=True)
        print("   ✅ Container Redis reiniciado.")
    except Exception as e:
        print(f"   ❌ Falha ao subir Docker: {e}")
    
    # 2. Patch no .env para evitar latência de DNS 'localhost' no Windows
    print("   [2/2] Otimizando arquivo .env...")
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Substitui localhost por 127.0.0.1 para drivers de conexão estáveis
        new_content = content.replace("localhost:6379", "127.0.0.1:6379")
        
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("   ✅ .env atualizado para 127.0.0.1")
    else:
        print("   ⚠️  Aviso: Arquivo .env não encontrado para patch.")

if __name__ == "__main__":
    kill_redis_zombies()
    stabilize_infra()
    print("\n✨ Infraestrutura estabilizada. Reinicie o servidor 'python run.py'.")
