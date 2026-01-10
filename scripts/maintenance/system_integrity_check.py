# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 02:30:00
import os
import sys
import socket
import json
import subprocess
from pathlib import Path
from decimal import Decimal

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(label, status, detail=""):
    color = Colors.GREEN if status == "OK" else Colors.RED if status == "FAIL" else Colors.YELLOW
    print(f"{Colors.BOLD}{label:<40}{Colors.ENDC} | {color}{status:<6}{Colors.ENDC} | {detail}")

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_integrity_check():
    print(f"\n{Colors.HEADER}🛡️  MesaFlow System Integrity Auditor v1.0{Colors.ENDC}")
    print("=" * 80)
    
    issues_found = 0
    warnings_found = 0

    # --- 1. AMBIENTE & CONFIGURAÇÃO ---
    print(f"\n{Colors.CYAN}[1/5] AMBIENTE & CONFIGURAÇÃO{Colors.ENDC}")
    env_path = Path(".env")
    example_path = Path(".env.example")
    
    if not env_path.exists():
        print_status("Arquivo .env", "FAIL", "Arquivo ausente na raiz.")
        issues_found += 1
    else:
        from dotenv import dotenv_values
        current = dotenv_values(env_path)
        expected = dotenv_values(example_path)
        missing = [k for k in expected.keys() if k not in current]
        if missing:
            print_status("Paridade .env", "FAIL", f"Faltam: {', '.join(missing)}")
            issues_found += 1
        else:
            print_status("Paridade .env", "OK")

    # --- 2. BACKEND & INFRA ---
    print(f"\n{Colors.CYAN}[2/5] BACKEND & INFRAESTRUTURA{Colors.ENDC}")
    if check_port(5432):
        print_status("PostgreSQL (5432)", "OK")
    else:
        print_status("PostgreSQL (5432)", "FAIL", "Servidor offline ou porta bloqueada.")
        issues_found += 1

    if check_port(6379):
        print_status("Redis (6379)", "OK")
    else:
        print_status("Redis (6379)", "WARN", "Offline. Cache e WebSockets em modo degradado.")
        warnings_found += 1

    # --- 3. FRONTEND INTEGRITY ---
    print(f"\n{Colors.CYAN}[3/5] FRONTEND INTEGRITY{Colors.ENDC}")
    fe_src = Path("frontend/src")
    syntax_err = 0
    if fe_src.exists():
        for p in fe_src.rglob("*.ts*"):
            try:
                content = p.read_text(encoding="utf-8")
                if content.startswith("# DOMAIN"):
                    syntax_err += 1
            except: continue
        
        if syntax_err > 0:
            print_status("Sintaxe de Metadados", "FAIL", f"{syntax_err} arquivos com '#' em vez de '//'")
            issues_found += 1
        else:
            print_status("Sintaxe de Metadados", "OK")
    
    if Path("frontend/node_modules").exists():
        print_status("Dependencias Frontend", "OK")
    else:
        print_status("Dependencias Frontend", "FAIL", "node_modules ausente.")
        issues_found += 1

    # --- 4. MOBILE INTEGRITY ---
    print(f"\n{Colors.CYAN}[4/5] MOBILE INTEGRITY{Colors.ENDC}")
    mob_assets = Path("mobile/assets")
    required_assets = ["icon.png", "splash.png", "adaptive-icon.png", "favicon.png"]
    missing_assets = [a for a in required_assets if not (mob_assets / a).exists()]
    
    if missing_assets:
        print_status("Assets Expo", "FAIL", f"Faltam: {', '.join(missing_assets)}")
        issues_found += 1
    else:
        print_status("Assets Expo", "OK")

    # --- 5. GOVERNANÇA & DOCS ---
    print(f"\n{Colors.CYAN}[5/5] GOVERNANÇA & DOCUMENTAÇÃO{Colors.ENDC}")
    tasks_path = Path("docs/TASKS.md")
    if tasks_path.exists():
        content = tasks_path.read_text(encoding="utf-8")
        pending = content.count("[ ]")
        print_status("Backlog (TASKS.md)", "OK", f"{pending} tarefas pendentes.")
    else:
        print_status("Backlog (TASKS.md)", "FAIL", "Arquivo mestre ausente.")
        issues_found += 1

    # --- RESULTADO FINAL ---
    print("\n" + "=" * 80)
    health = max(0, 100 - (issues_found * 20) - (warnings_found * 5))
    print(f"{Colors.BOLD}SAÚDE DO SISTEMA: {health}%{Colors.ENDC}")
    print(f"Erros Críticos: {Colors.RED}{issues_found}{Colors.ENDC} | Avisos: {Colors.YELLOW}{warnings_found}{Colors.ENDC}")
    print("=" * 80)

    if issues_found > 0:
        print(f"\n{Colors.RED}🚨 O sistema possui inconsistências que podem impedir a operação.{Colors.ENDC}")
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}✨ Sistema íntegro e pronto para produção.{Colors.ENDC}")
        sys.exit(0)

if __name__ == "__main__":
    run_integrity_check()
