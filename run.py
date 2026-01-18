# DOMAIN: DEVOPS
# LAST_MODIFIED: 2026-01-16 05:15:00
import subprocess
import sys
import os
import time
import socket
import signal
from pathlib import Path

# Configuração
BACKEND_PORT = 8000
FRONTEND_PORT = 3000
HOST = "127.0.0.1"

class MesaFlowLauncher:
    def __init__(self):
        self.processes = []
        self.is_windows = sys.platform == "win32"
        self.root_dir = Path(os.getcwd())

    def log(self, msg, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARN": "⚠️", "ERROR": "❌", "SYSTEM": "⚙️"}
        print(f"{icons.get(level, '')}  [{level}] {msg}")

    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((HOST, port)) == 0

    def kill_process_on_port(self, port):
        """Mata cirurgicamente o processo na porta específica."""
        if not self.is_port_in_use(port):
            return

        self.log(f"Liberando porta {port}...", "SYSTEM")
        try:
            if self.is_windows:
                # Encontra PID e mata apenas ele
                cmd = f"for /f \"tokens=5\" %a in ('netstat -aon ^| find \":{port}\" ^| find \"LISTENING\"') do taskkill /f /pid %a"
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(f"lsof -ti:{port} | xargs kill -9", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Aguarda liberação
            time.sleep(1)
        except Exception as e:
            self.log(f"Falha ao liberar porta {port}: {e}", "WARN")

    def wait_for_service(self, port, name, timeout=30):
        """Aguarda o serviço estar disponível via TCP."""
        self.log(f"Aguardando {name} iniciar na porta {port}...", "INFO")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_port_in_use(port):
                self.log(f"{name} está ONLINE!", "SUCCESS")
                return True
            time.sleep(0.5)
        self.log(f"Timeout aguardando {name}.", "ERROR")
        return False

    def install_frontend_deps(self):
        frontend_dir = self.root_dir / "frontend"
        node_modules = frontend_dir / "node_modules"
        
        if not node_modules.exists():
            self.log("Instalando dependências do Frontend (Primeira execução)...", "SYSTEM")
            npm = "npm.cmd" if self.is_windows else "npm"
            try:
                subprocess.run([npm, "install"], cwd=frontend_dir, check=True, shell=self.is_windows)
            except subprocess.CalledProcessError:
                self.log("Falha no npm install.", "ERROR")
                sys.exit(1)

    def start(self):
        print("========================================")
        print("🚀 MESAFLOW OS - LAUNCHER v2.0 (L6)")
        print("========================================")

        # 1. Limpeza Cirúrgica
        self.kill_process_on_port(BACKEND_PORT)
        self.kill_process_on_port(FRONTEND_PORT)

        # 2. Dependências
        self.install_frontend_deps()

        # 3. Iniciar Backend
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)
        env["PYTHONIOENCODING"] = "utf-8" # Fix Windows Unicode

        self.log("Iniciando Backend (FastAPI)...", "INFO")
        backend_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", HOST, "--port", str(BACKEND_PORT)]
        
        # Popen não bloqueia e nos dá o PID
        backend_proc = subprocess.Popen(backend_cmd, env=env, cwd=self.root_dir)
        self.processes.append(backend_proc)

        # 4. Aguardar Backend (Healthcheck real)
        if not self.wait_for_service(BACKEND_PORT, "Backend"):
            self.shutdown()
            sys.exit(1)

        # 5. Iniciar Frontend
        self.log("Iniciando Frontend (Next.js)...", "INFO")
        npm = "npm.cmd" if self.is_windows else "npm"
        frontend_cmd = [npm, "run", "dev"]
        
        frontend_proc = subprocess.Popen(frontend_cmd, cwd=self.root_dir / "frontend", shell=self.is_windows)
        self.processes.append(frontend_proc)

        self.log("Sistema Operacional. Pressione CTRL+C para parar.", "SUCCESS")
        
        # 6. Monitoramento
        try:
            while True:
                time.sleep(1)
                # Verifica se algum processo morreu inesperadamente
                if backend_proc.poll() is not None:
                    self.log("Backend morreu inesperadamente.", "ERROR")
                    break
                if frontend_proc.poll() is not None:
                    self.log("Frontend morreu inesperadamente.", "ERROR")
                    break
        except KeyboardInterrupt:
            self.log("Parando serviços...", "WARN")
        finally:
            self.shutdown()

    def shutdown(self):
        """Encerra processos filhos de forma limpa."""
        for p in self.processes:
            if p.poll() is None: # Se ainda está rodando
                if self.is_windows:
                    # Windows precisa de taskkill forçado para árvores de processo (npm -> node)
                    subprocess.run(f"taskkill /F /T /PID {p.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    p.terminate()
        self.log("MesaFlow encerrado.", "SUCCESS")

if __name__ == "__main__":
    launcher = MesaFlowLauncher()
    launcher.start()

