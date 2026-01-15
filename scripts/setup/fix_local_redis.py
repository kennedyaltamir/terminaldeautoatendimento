
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 16:15:00
import os
import sys
import subprocess
import time
from pathlib import Path

# Tenta importar redis, se não tiver, avisa
try:
    import redis
except ImportError:
    print("❌ Biblioteca 'redis' não instalada. Rodando pip install...")
    subprocess.run([sys.executable, "-m", "pip", "install", "redis"])
    import redis

ENV_PATH = Path(".env")

def run_command(cmd):
    try:
        return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        return None

def start_docker_redis():
    print("🐳 [1/3] Verificando Docker Redis...")
    
    # 1. Verifica se o Docker está rodando
    check = run_command("docker ps")
    if not check:
        print("   ❌ Docker não parece estar rodando. Abra o Docker Desktop e tente novamente.")
        return False

    # 2. Verifica se o container já existe
    container_name = "mesaflow-redis"
    check_container = run_command(f"docker ps -a -q -f name={container_name}")
    
    if check_container and check_container.stdout.strip():
        print(f"   🔄 Reiniciando container '{container_name}'...")
        run_command(f"docker start {container_name}")
    else:
        print(f"   🚀 Criando container '{container_name}'...")
        run_command(f"docker run -d -p 6379:6379 --name {container_name} redis:alpine")
    
    print("   ✅ Container Redis ativo.")
    return True

def patch_env_file():
    print("📝 [2/3] Configurando .env para Localhost...")
    
    if not ENV_PATH.exists():
        print("   ❌ Arquivo .env não encontrado.")
        return False

    content = ENV_PATH.read_text(encoding="utf-8")
    new_lines = []
    redis_patched = False
    
    local_url = "redis://localhost:6379/0"

    for line in content.splitlines():
        if line.startswith("REDIS_URL="):
            # Comenta a linha antiga se não for localhost
            if "localhost" not in line and "127.0.0.1" not in line:
                new_lines.append(f"# {line} # (Comentado pelo Auto-Fix)")
            new_lines.append(f"REDIS_URL={local_url}")
            redis_patched = True
        else:
            new_lines.append(line)
    
    if not redis_patched:
        new_lines.append(f"REDIS_URL={local_url}")

    # Remove duplicatas consecutivas causadas pelo loop
    final_content = []
    for line in new_lines:
        if not final_content or final_content[-1] != line:
            final_content.append(line)

    ENV_PATH.write_text("\n".join(final_content), encoding="utf-8")
    print(f"   ✅ .env atualizado: REDIS_URL={local_url}")
    return True

def test_connection():
    print("🔌 [3/3] Testando Conexão...")
    time.sleep(2) # Espera o container subir
    try:
        r = redis.from_url("redis://localhost:6379/0", socket_connect_timeout=2)
        if r.ping():
            print("   ✨ SUCESSO: Redis conectado e respondendo PONG!")
            return True
    except Exception as e:
        print(f"   ❌ Falha na conexão: {e}")
        return False

if __name__ == "__main__":
    print("========================================")
    print("🔧 MESAFLOW REDIS AUTO-FIX")
    print("========================================")
    
    if start_docker_redis():
        if patch_env_file():
            if test_connection():
                print("\n🏆 Redis Configurado. Reinicie o servidor (run.py) para aplicar.")
            else:
                print("\n⚠️  Docker subiu, mas a conexão falhou. Verifique firewall/portas.")
        else:
            print("\n❌ Falha ao editar .env")
    else:
        print("\n❌ Falha no Docker. Certifique-se que o Docker Desktop está aberto.")

