import subprocess
import sys
import time
import socket
import os

def log(msg, level="INFO"):
    print(f"[{level}] {msg}")

def check_port(host, port, timeout=2):
    """Verifica se uma porta TCP está aberta."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((host, port))
        return result == 0
    except Exception:
        return False
    finally:
        s.close()

def run_docker_cmd(cmd_list):
    """Executa comando docker com compatibilidade Windows."""
    try:
        # shell=True é crucial no Windows para encontrar o executável no PATH
        is_windows = sys.platform == "win32"
        result = subprocess.run(
            cmd_list, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            shell=is_windows,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except FileNotFoundError:
        return False, "Comando 'docker' não encontrado no PATH."

def cleanup_conflicts():
    """Remove containers que podem estar bloqueando a porta."""
    conflicts = ["mesaflow-redis", "redis", "mesaflow-redis-"]
    log("🧹 Limpando containers conflitantes...")
    
    for name in conflicts:
        # Tenta parar e remover, ignorando erros se não existir
        run_docker_cmd(["docker", "rm", "-f", name])

def start_redis_container():
    """Tenta iniciar o container Redis via Docker."""
    container_name = "mesaflow-redis"
    
    # 1. Limpeza prévia
    cleanup_conflicts()
    
    log(f"🚀 Iniciando novo container '{container_name}'...")
    
    # 2. Sobe novo container
    success, output = run_docker_cmd([
        "docker", "run", "-d",
        "-p", "6379:6379",
        "--name", container_name,
        "redis:alpine"
    ])
    
    if success:
        return True
    else:
        log(f"❌ Falha ao subir container: {output}", "ERROR")
        return False

def update_env_file():
    """Garante que o .env aponte para localhost."""
    env_path = ".env"
    if not os.path.exists(env_path):
        log(".env não encontrado. Criando padrão...", "WARN")
        with open(env_path, "w") as f:
            f.write("REDIS_HOST=127.0.0.1\nREDIS_PORT=6379\n")
        return

    with open(env_path, "r") as f:
        lines = f.readlines()
    
    new_lines = []
    updated = False
    for line in lines:
        if line.startswith("REDIS_HOST="):
            new_lines.append("REDIS_HOST=127.0.0.1\n")
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append("\nREDIS_HOST=127.0.0.1\n")
        new_lines.append("REDIS_PORT=6379\n")
    
    with open(env_path, "w") as f:
        f.writelines(new_lines)
    
    log(".env configurado para REDIS_HOST=127.0.0.1")

def main():
    log("🔍 Diagnóstico de Infraestrutura Redis (v2.1 Windows Fix)...")

    # PASSO 1: Verificar Docker Daemon
    log("🐳 Verificando Docker Daemon...")
    docker_ok, docker_err = run_docker_cmd(["docker", "info"])
    
    if not docker_ok:
        log(f"❌ Docker não detectado. Erro: {docker_err}", "FATAL")
        log("   DICA: Abra o Docker Desktop e aguarde a inicialização.", "FATAL")
        sys.exit(1)
    else:
        log("✅ Docker Daemon detectado e operante.")

    # PASSO 2: Verificar Porta
    if check_port("127.0.0.1", 6379):
        log("⚠️  Porta 6379 já está aberta. Verificando se é o container correto...")
        # Se a porta está aberta, pode ser um container antigo ou instalação nativa.
        # Vamos tentar limpar para garantir estado limpo.
        cleanup_conflicts()
        time.sleep(2) # Espera liberar a porta
    
    # PASSO 3: Subir Container Oficial
    if start_redis_container():
        log("⏳ Aguardando boot do Redis (5s)...")
        time.sleep(5)
        
        if check_port("127.0.0.1", 6379):
            log("✅ Infraestrutura Redis estabilizada com sucesso!")
            update_env_file()
            sys.exit(0)
        else:
            log("❌ Container subiu, mas porta 6379 não responde. Verifique Firewall.", "FATAL")
            sys.exit(1)
    else:
        log("❌ Não foi possível iniciar o Redis.", "FATAL")
        sys.exit(1)

if __name__ == "__main__":
    main()

