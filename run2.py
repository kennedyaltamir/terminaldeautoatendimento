# DOMAIN: DEVOPS
# DESCRIPTION: Gerenciador de Serviços MesaFlow v5.0 - Persistent Watchdog.
# FIX: Removido limite de reinício para manter o ambiente sempre ativo.

import subprocess
import sys
import os
import time
import socket
import signal
from pathlib import Path

class MesaFlowLauncher:
    def __init__(self):
        self.processes = {}
        self.is_windows = sys.platform == "win32"
        self.root_dir = Path(os.getcwd())
        self.should_exit = False
        
        # Configura sinal de interrupção (Ctrl+C)
        signal.signal(signal.SIGINT, self.handle_exit)

    def log(self, msg, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARN": "⚠️", "ERROR": "❌", "SYSTEM": "⚙️"}
        print(f"{icons.get(level, ' ')}  [{level}] {msg}")

    def handle_exit(self, signum, frame):
        self.log("Encerrando serviços MesaFlow...", "WARN")
        self.should_exit = True
        self.shutdown()
        sys.exit(0)

    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", port)) == 0

    def start_backend(self):
        self.log("Iniciando Backend (Porta 8000)...", "SYSTEM")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)
        env["PYTHONIOENCODING"] = "utf-8"
        cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
        return subprocess.Popen(cmd, env=env, cwd=self.root_dir)

    def start_frontend(self):
        self.log("Iniciando Frontend (Porta 3000)...", "SYSTEM")
        npm = "npm.cmd" if self.is_windows else "npm"
        return subprocess.Popen([npm, "run", "dev"], cwd=self.root_dir / "frontend", shell=self.is_windows)

    def shutdown(self):
        for name, proc in self.processes.items():
            if proc.poll() is None:
                if self.is_windows:
                    subprocess.run(f"taskkill /F /T /PID {proc.pid}", shell=True, capture_output=True)
                else:
                    proc.terminate()
        self.log("Todos os serviços foram parados.", "SUCCESS")

    def start(self):
        print("="*50)
        print("🚀 MESAFLOW OS - PERSISTENT SERVICE MANAGER v5.0")
        print("="*50)
        
        self.processes["Backend"] = self.start_backend()
        self.processes["Frontend"] = self.start_frontend()

        self.log("Sistema operacional em execução. Mantenha esta janela aberta.", "SUCCESS")
        self.log("Pressione Ctrl+C para encerrar tudo.", "INFO")

        while not self.should_exit:
            time.sleep(5)
            for name, proc in self.processes.items():
                if proc.poll() is not None:
                    self.log(f"⚠️ {name} caiu! Reiniciando automaticamente...", "ERROR")
                    if name == "Backend": self.processes[name] = self.start_backend()
                    else: self.processes[name] = self.start_frontend()

if __name__ == "__main__":
    MesaFlowLauncher().start()