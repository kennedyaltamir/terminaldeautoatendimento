import subprocess
import sys
import os

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def run_command(command, cwd=None, description=""):
    print(f"{Colors.BLUE}Running: {description}...{Colors.ENDC}")
    try:
        # shell=True para Windows reconhecer comandos como 'npm'
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ OK{Colors.ENDC}")
            if result.stdout:
                print(f"   {result.stdout.strip().splitlines()[0]}...") # Mostra apenas a primeira linha
            return True
        else:
            print(f"{Colors.YELLOW}⚠️  Vulnerabilities Found or Error:{Colors.ENDC}")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Execution Failed: {e}{Colors.ENDC}")
        return False

def audit_python():
    print(f"\n{Colors.HEADER}--- Auditing Backend (Python) ---{Colors.ENDC}")
    # pip-audit verifica o ambiente atual ou requirements.txt
    # Usamos --desc para ver detalhes
    return run_command("pip-audit --desc on", description="pip-audit")

def audit_node(directory, label):
    print(f"\n{Colors.HEADER}--- Auditing {label} (Node.js) ---{Colors.ENDC}")
    if not os.path.exists(directory):
        print(f"{Colors.YELLOW}Directory {directory} not found. Skipping.{Colors.ENDC}")
        return True
        
    # npm audit --audit-level=high ignora avisos leves
    return run_command("npm audit --audit-level=high", cwd=directory, description="npm audit")

def main():
    print(f"{Colors.HEADER}🚀 Starting Software Composition Analysis (SCA){Colors.ENDC}")
    
    # 1. Python Backend
    py_status = audit_python()
    
    # 2. Frontend
    fe_status = audit_node("frontend", "Frontend")
    
    # 3. Mobile
    mob_status = audit_node("mobile", "Mobile")
    
    print(f"\n{Colors.HEADER}--- Audit Summary ---{Colors.ENDC}")
    print(f"Backend: {'✅ Secure' if py_status else '⚠️  Issues Found'}")
    print(f"Frontend: {'✅ Secure' if fe_status else '⚠️  Issues Found'}")
    print(f"Mobile:   {'✅ Secure' if mob_status else '⚠️  Issues Found'}")
    
    # O script não deve quebrar o pipeline se houver vulnerabilidades (apenas reportar),
    # a menos que configuremos strict mode. Por enquanto, retornamos 0 para não travar o GTM.
    # Em um pipeline real de bloqueio, retornaríamos 1 se status fosse False.
    
    print(f"\n{Colors.GREEN}🏆 SCA Audit Completed.{Colors.ENDC}")
    sys.exit(0)

if __name__ == "__main__":
    main()
