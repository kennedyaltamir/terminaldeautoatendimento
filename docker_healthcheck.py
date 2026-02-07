

import subprocess
import time
import sys
import os
import socket
import csv

def log(msg, level="INFO"):
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "WARN": "\033[93m", "FAIL": "\033[91m", "END": "\033[0m"}
    ts = time.strftime("%H:%M:%S")
    print(f"{colors.get(level, '')}[{level}] [{ts}] {msg}{colors['END']}")

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def is_docker_ok():
    r = run("docker info")
    return "Server Version" in r.stdout

def kill_safe_python():
    """
    Mata todos os processos python.exe EXCETO o atual.
    """
    current_pid = os.getpid()
    try:
        # Lista processos Python em formato CSV
        cmd = 'tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if "INFO: No tasks are running" in result.stdout:
            return

        # Parseia o CSV manual
        lines = result.stdout.strip().splitlines()
        for line in lines:
            # Formato: "python.exe","1234","Console","1","10,000 K"
            parts = line.split(',')
            if len(parts) >= 2:
                pid_str = parts[1].strip('"')
                if pid_str.isdigit():
                    pid = int(pid_str)
                    if pid != current_pid:
                        run(f'taskkill /F /PID {pid}')
    except Exception as e:
        log(f"Erro ao limpar Python: {e}", "WARN")

def kill_project_processes():
    """
    Encerra processos de desenvolvimento liberando portas.
    """
    log("🧹 Higienizando ambiente (Matando Node, Uvicorn e Python zumbis)...", "WARN")
    
    # 1. Mata processos que não são o próprio script
    targets = ["node.exe", "npm.exe", "uvicorn.exe", "celery.exe"]
    for proc in targets:
        run(f'taskkill /F /IM "{proc}" /T 2>nul')
    
    # 2. Mata Python com segurança (preservando este script)
    kill_safe_python()
    
    log("Processos de aplicação encerrados.", "OK")

def kill_everything_docker():
    log("Iniciando purga de processos remanescentes do Docker...", "WARN")
    zombies = [
        "Docker Desktop.exe", 
        "com.docker.backend.exe", 
        "com.docker.build.exe", 
        "com.docker.proxy.exe",
        "com.docker.vpnkit.exe",
        "com.docker.extensions.exe",
        "com.docker.dev-envs.exe",
        "docker-index.exe"
    ]
    for proc in zombies:
        run(f'taskkill /F /IM "{proc}" /T 2>nul')
    log("Memória do Docker higienizada.", "OK")

def main():
    # 1. Purga de Aplicação Segura
    kill_project_processes()

    if is_docker_ok():
        log("Docker já está operacional.", "OK")
        return

    log("DOCKER TRAVADO DETECTADO. Iniciando rito de restauração agressiva.", "FAIL")

    # 2. Parar serviço Windows
    log("Parando serviço 'com.docker.service'...", "INFO")
    run("sc.exe stop com.docker.service")

    # 3. Matar zumbis do Docker
    kill_everything_docker()

    # 4. Resetar WSL
    log("Reiniciando subsistema WSL...", "WARN")
    run("wsl --shutdown")
    time.sleep(2)

    # 5. Reiniciar serviço Windows
    log("Subindo serviço 'com.docker.service'...", "INFO")
    run("sc.exe start com.docker.service")

    # 6. Lançar UI
    docker_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if os.path.exists(docker_path):
        log("Lançando Docker Desktop UI...")
        os.startfile(docker_path)
    else:
        log("Executável não encontrado.", "FAIL")
        return

    # 7. Polling
    log("Aguardando estabilização do motor...")
    for i in range(40):
        if is_docker_ok():
            print("\n")
            log("✅ DOCKER RESTAURADO COM SUCESSO!", "OK")
            log("O Redis agora deve subir normalmente no 'run.py'.", "OK")
            return
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(3)

    print("\n")
    log("❌ Falha ao restaurar. Tente abrir o Docker Desktop como Administrador.", "FAIL")

if __name__ == "__main__":
    main()
