import subprocess
import sys
import os
import platform
import time
import shutil
from threading import Thread

def is_windows():
    return platform.system() == "Windows"

def kill_port(port):
    """Mata qualquer processo ocupando a porta especificada."""
    if is_windows():
        command = f"for /f \"tokens=5\" %a in ('netstat -aon ^| find \":{port}\" ^| find \"LISTENING\"') do taskkill /f /pid %a"
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(f"lsof -ti:{port} | xargs kill -9", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def kill_zombie_processes():
    """Limpeza agressiva de processos Node e Python."""
    print("💀 Higienizando ambiente (Matando processos antigos)...")
    kill_port(8000)
    kill_port(3000)
    
    if is_windows():
        subprocess.run("taskkill /F /IM node.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("taskkill /F /IM uvicorn.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run("pkill -f node", shell=True)
        subprocess.run("pkill -f uvicorn", shell=True)
    time.sleep(1)

def install_frontend_deps():
    """Garante que node_modules existe."""
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    node_modules = os.path.join(frontend_dir, "node_modules")
    
    if not os.path.exists(node_modules):
        print("📦 Instalando dependências do Frontend (pode demorar)...")
        npm_cmd = "npm.cmd" if is_windows() else "npm"
        subprocess.run([npm_cmd, "install"], cwd=frontend_dir, check=True)

def run_backend():
    print("🚀 Iniciando Backend (Porta 8000)...")
    # Adiciona o diretório atual ao PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        env=env
    )

def run_frontend():
    print("🎨 Iniciando Frontend (Porta 3000)...")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    npm_cmd = "npm.cmd" if is_windows() else "npm"
    
    subprocess.run([npm_cmd, "run", "dev"], cwd=frontend_dir)

if __name__ == "__main__":
    print("🔥 Inicializando MesaFlow (Modo Estável Windows)...")
    
    kill_zombie_processes()
    install_frontend_deps()

    backend_thread = Thread(target=run_backend)
    frontend_thread = Thread(target=run_frontend)

    backend_thread.start()
    time.sleep(2) # Dá um tempo para o backend subir o socket
    frontend_thread.start()

    try:
        backend_thread.join()
        frontend_thread.join()
    except KeyboardInterrupt:
        print("\n🛑 Encerrando...")
        kill_zombie_processes()
        sys.exit(0)