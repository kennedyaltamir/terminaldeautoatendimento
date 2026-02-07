# DOMAIN: ROOT_CONFIG
# VERSION: v13.1.1 - THE SENTINEL PROTOCOL (PORT BYPASS EDITION)
# DESCRIPTION: Agente de Autocura com correção de AttributeError e bypass da porta 8000 para 8001.
# DNA_ID: MF-SENTINEL-V13-1-1-GOLD
# LAST_MODIFIED: 2026-01-30 06:30:00

import subprocess
import sys
import os
import time
import socket
import signal
import platform
import shutil
import json
import argparse
import urllib.request
import threading
import uuid
import re
import zipfile
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

# --- ENUMS DE GOVERNANÇA ---
class IncidentSeverity(str, Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class RootCause(str, Enum):
    CONFIG_ERROR = "SYS-CONFIG-ERROR"
    PORT_CONFLICT = "SYS-PORT-CONFLICT"
    DOCKER_DOWN = "SYS-DOCKER-DOWN"
    REDIS_FAIL = "SYS-REDIS-FAIL"
    DEPENDENCY_MISSING = "SYS-DEP-MISSING"
    CODE_CRASH = "APP-CODE-CRASH"
    HEALTHCHECK_TIMEOUT = "APP-HC-TIMEOUT"
    SYSTEMIC_FAILURE = "SYS-LOGIC-FAILURE"
    UNKNOWN = "UNKNOWN"

# --- ESTILIZAÇÃO ---
class Colors:
    RED_BOLD = '\033[1;31m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW_BOLD = '\033[1;33m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    ENDC = '\033[0m'

# --- MEMÓRIA OPERACIONAL ---
class ForensicKB:
    def __init__(self):
        self.path = Path("scripts/knowledge/forensic_kb.json")
        self.data = self._load()

    def _load(self):
        if self.path.exists():
            try: return json.loads(self.path.read_text())
            except: pass
        return {"history": {}, "stats": {"total_repairs": 0, "success_rate": 0.0}}

    def record_fix(self, cause: RootCause, success: bool):
        c = cause.value
        if c not in self.data["history"]:
            self.data["history"][c] = {"attempts": 0, "successes": 0}
        self.data["history"][c]["attempts"] += 1
        if success: self.data["history"][c]["successes"] += 1
        self.data["stats"]["total_repairs"] += 1
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2))

# --- MOTOR FORENSE ---
class ErrorForensicsManager:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.base_dir = Path("ERROSDETECTADOS")
        self.timeline = deque(maxlen=500)
        self.kb = ForensicKB()

    def add_event(self, msg: str, type: str = "SYSTEM", metadata: dict = None):
        event = {"ts": datetime.now(timezone.utc).isoformat(), "type": type, "msg": msg, "meta": metadata}
        self.timeline.append(event)

    def classify_error(self, msg: str) -> RootCause:
        patterns = [
            (r"address.*already.*use|port.*occupied|10013", RootCause.PORT_CONFLICT),
            (r"docker.*daemon.*not.*running", RootCause.DOCKER_DOWN),
            (r"redis.*connection.*refused|10061|timeout.*connecting", RootCause.REDIS_FAIL),
            (r"npm.*not.*found|node_modules", RootCause.DEPENDENCY_MISSING),
            (r"syntaxerror|attributeerror|traceback|exception", RootCause.CODE_CRASH),
        ]
        for pat, cause in patterns:
            if re.search(pat, msg.lower()): return cause
        return RootCause.UNKNOWN

    def capture_incident(self, code: str, message: str, severity: IncidentSeverity, component: str):
        ts = datetime.now(timezone.utc)
        incident_dir = self.base_dir / ts.strftime("%Y-%m-%d") / f"{ts.strftime('%H-%M-%S')}_{code}"
        incident_dir.mkdir(parents=True, exist_ok=True)
        cause = self.classify_error(message)
        tech_report = {
            "session_id": self.session_id, "timestamp": ts.isoformat(), "severity": severity.value,
            "component": component, "root_cause": cause.value, "message": message, "timeline": list(self.timeline)
        }
        (incident_dir / "technical_forensic.json").write_text(json.dumps(tech_report, indent=2))
        return cause

# --- ORQUESTRADOR AGENTE ---
class Orchestrator:
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.forensics = ErrorForensicsManager(self.session_id)
        self.running = True
        self.procs = {}
        self.restarts = {"Backend": 0, "Frontend": 0}
        self.boot_time = time.time()
        
        # 🛡️ BYPASS: Porta 8001 para evitar WinError 10013 na 8000
        self.be_port = 8001 
        self.fe_port = 3000
        self.health_url = f"http://127.0.0.1:{self.be_port}/api/health"

        self.FIX_MATRIX = {
            RootCause.PORT_CONFLICT: self._fix_port_conflict,
            RootCause.REDIS_FAIL: self._fix_redis,
            RootCause.DOCKER_DOWN: self._fix_redis,
            RootCause.DEPENDENCY_MISSING: self._fix_deps
        }

        signal.signal(signal.SIGINT, lambda s, f: self.shutdown())

    def log(self, msg: str, severity: IncidentSeverity = IncidentSeverity.INFO, prefix: str = "SENTINEL"):
        color = {IncidentSeverity.CRITICAL: Colors.RED_BOLD, IncidentSeverity.ERROR: Colors.RED, 
                 IncidentSeverity.WARNING: Colors.YELLOW, IncidentSeverity.SUCCESS: Colors.GREEN}.get(severity, Colors.BLUE)
        print(f"{color}[{prefix}] [{severity.value}] {msg.strip()}{Colors.ENDC}")

    def _stream_reader(self, name: str, stream):
        for line in iter(stream.readline, ''):
            if not line: break
            self._analyze_log_line(name, line)
        stream.close()

    def _analyze_log_line(self, name: str, line: str):
        line_lower = line.lower()
        severity = IncidentSeverity.INFO
        if any(x in line_lower for x in ["error", "exception", "traceback", "failed to load"]):
            severity = IncidentSeverity.ERROR
        elif any(x in line_lower for x in ["warning", "timeout", "retry"]):
            severity = IncidentSeverity.WARNING_DEGRADED
        elif any(x in line_lower for x in ["started", "ready", "200 ok", "compiled successfully"]):
            severity = IncidentSeverity.SUCCESS
        self.log(line, severity, prefix=name.upper())

    def _fix_port_conflict(self):
        self.log(f"Higienizando portas {self.be_port}/{self.fe_port}...", IncidentSeverity.WARNING)
        for port in [self.be_port, self.fe_port, 8000]:
            if sys.platform == "win32":
                subprocess.run(f"for /f \"tokens=5\" %a in ('netstat -aon ^| find \":{port}\" ^| find \"LISTENING\"') do taskkill /f /pid %a /t", shell=True, capture_output=True)
        time.sleep(1)
        return True

    def _fix_redis(self):
        d_info = subprocess.run("docker info", shell=True, capture_output=True)
        if d_info.returncode != 0: return False
        self.log("Reiniciando container Redis...", IncidentSeverity.WARNING_INFRA)
        subprocess.run("docker restart mesaflow_redis", shell=True, capture_output=True)
        time.sleep(2)
        return self._check_port(6379)

    def _fix_deps(self):
        npm = "npm.cmd" if sys.platform == "win32" else "npm"
        subprocess.run([npm, "install"], cwd="./frontend", shell=(sys.platform == "win32"))
        return True

    def _check_port(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", port)) == 0

    def _semantic_healthcheck(self) -> bool:
        if time.time() - self.boot_time < 25: return True
        try:
            with urllib.request.urlopen(self.health_url, timeout=5) as r:
                data = json.loads(r.read())
                return data.get("status") in ("healthy", "degraded", "bypass", "operational")
        except: return False

    def start(self):
        self.log(f"Sentinel Sovereign {self.session_id} Iniciado", IncidentSeverity.SUCCESS)
        self._fix_port_conflict()
        self._launch_backend()
        self._launch_frontend()
        try:
            while self.running:
                time.sleep(5)
                for name, proc in list(self.procs.items()):
                    if proc.poll() is not None:
                        self.log(f"Processo {name} caiu. Reiniciando...", IncidentSeverity.ERROR)
                        if name == "Backend": self._launch_backend()
                        else: self._launch_frontend()
        except KeyboardInterrupt: self.shutdown()

    def check_redis():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex(('127.0.0.1', 6379)) != 0:
                return False
            try:
                res = subprocess.run("docker exec mesaflow_redis redis-cli ping", shell=True, capture_output=True, text=True)
                return "PONG" in res.stdout
            except:
                return False

    def start():
        print("\033[94m[SENTINEL] Iniciando Protocolo de Boot Soberano...\033[0m")
        
        # 1. Aguarda Redis (Mandatório)
        print("[SENTINEL] Validando dependências críticas: REDIS")
        retries = 0
        while not check_redis() and retries < 5:
            print(f"⚠️ Redis offline. Tentando subir via Compose (Tentativa {retries+1}/5)...")
            subprocess.run("docker-compose up -d redis", shell=True)
            time.sleep(5)
            retries += 1
        
        if not check_redis():
            print("\033[91m[FAIL] REDIS inacessível. Execute 'python scripts/infra/docker_guardian.py' primeiro.\033[0m")
            sys.exit(1)
        
        print("\033[92m[OK] REDIS Detectado. Lançando Kernel...\033[0m")
        
        # 2. Lança Backend e Frontend
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        be = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001", "--reload"], env=env)
        fe = subprocess.Popen(["npm", "run", "dev"], cwd="./frontend", shell=True)
        
        try:
            while True:
                time.sleep(1)
                if be.poll() is not None or fe.poll() is not None:
                    print("🚨 Falha em processo crítico. Reiniciando...")
                    break
        except KeyboardInterrupt:
            be.terminate()
            fe.terminate()
def check_redis():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex(('127.0.0.1', 6379)) != 0:
            return False
        try:
            res = subprocess.run("docker exec mesaflow_redis redis-cli ping", shell=True, capture_output=True, text=True)
            return "PONG" in res.stdout
        except:
            return False

def start():
    print("\033[94m[SENTINEL] Iniciando Protocolo de Boot Soberano...\033[0m")
    
    # 1. Aguarda Redis (Mandatório)
    print("[SENTINEL] Validando dependências críticas: REDIS")
    retries = 0
    while not check_redis() and retries < 5:
        print(f"⚠️ Redis offline. Tentando subir via Compose (Tentativa {retries+1}/5)...")
        subprocess.run("docker-compose up -d redis", shell=True)
        time.sleep(5)
        retries += 1
    
    if not check_redis():
        print("\033[91m[FAIL] REDIS inacessível. Execute 'python scripts/infra/docker_guardian.py' primeiro.\033[0m")
        sys.exit(1)
    
    print("\033[92m[OK] REDIS Detectado. Lançando Kernel...\033[0m")
    
    # 2. Lança Backend e Frontend
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    be = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001", "--reload"], env=env)
    fe = subprocess.Popen(["npm", "run", "dev"], cwd="./frontend", shell=True)
    
    try:
        while True:
            time.sleep(1)
            if be.poll() is not None or fe.poll() is not None:
                print("🚨 Falha em processo crítico. Reiniciando...")
                break
    except KeyboardInterrupt:
        be.terminate()
        fe.terminate()

if __name__ == "__main__":
    start()
    if __name__ == "__main__":
        start()

    def _launch_backend(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(self.be_port), "--reload"]
        self.procs["Backend"] = subprocess.Popen(cmd, env=env, shell=(sys.platform == "win32"))

    def _launch_frontend(self):
        env = os.environ.copy()
        env["NEXT_PUBLIC_API_URL"] = f"http://127.0.0.1:{self.be_port}/api"
        env["NEXT_PUBLIC_WS_URL"] = f"ws://127.0.0.1:{self.be_port}/api/ws"
        cmd = ["npm", "run", "dev"]
        self.procs["Frontend"] = subprocess.Popen(cmd, env=env, cwd="./frontend", shell=(sys.platform == "win32"))

    def shutdown(self):
        self.running = False
        for p in self.procs.values(): p.terminate()
        sys.exit(0)

if __name__ == "__main__":
    Orchestrator().start()
