import subprocess
import sys
import os
import io
from pathlib import Path

# [TEST_EXEMPT: Script de orquestração de auditoria - Windows UTF-8 Patch]

# Força UTF-8 no terminal Windows para evitar UnicodeEncodeError com emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def run_step(command, description):
    print(f"{Colors.BLUE}🔄 {description}...{Colors.ENDC}")
    
    # Injeta variável de ambiente para forçar UTF-8 nos processos filhos
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Sucesso!{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.FAIL}❌ Falha no passo: {description}{Colors.ENDC}")
            if result.stdout: print(result.stdout)
            if result.stderr: print(result.stderr)
            return False
    except Exception as e:
        print(f"{Colors.FAIL}💥 Erro inesperado: {e}{Colors.ENDC}")
        return False

def main():
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.HEADER}   MESAFLOW MASTER ALIGNMENT CHECK (v1.1)         {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}\n")

    steps = [
        ("python scripts/setup/verify_installation.py", "Verificando Integridade de Arquivos"),
        ("python scripts/maintenance/check_mobile_readiness.py", "Validando Banco de Dados para Mobile"),
        ("python scripts/setup/verify_mobile_master.py", "Auditando Lógica de Missões Mobile"),
        ("python scripts/setup/verify_sync_final.py", "Checando Prontidão para Handover"),
    ]

    failed_steps = []
    for cmd, desc in steps:
        if not run_step(cmd, desc):
            failed_steps.append(desc)
        print("-" * 50)

    if not failed_steps:
        print(f"\n{Colors.GREEN}🏆 SISTEMA TOTALMENTE ALINHADO E PRONTO PARA O APK!{Colors.ENDC}")
    else:
        print(f"\n{Colors.YELLOW}⚠️  ALINHAMENTO PARCIAL. Falhas detectadas em:{Colors.ENDC}")
        for f in failed_steps:
            print(f"  - {f}")
        print(f"\n{Colors.BLUE}Dica: Verifique se o seu .env está configurado corretamente.{Colors.ENDC}")

if __name__ == "__main__":
    main()
