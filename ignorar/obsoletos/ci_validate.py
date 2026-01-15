import subprocess
import sys
import os

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def run_command(command, description, cwd=None):
    print(f"\n{Colors.HEADER}🚀 Executando: {description}...{Colors.ENDC}")
    try:
        # Shell=True necessário para comandos compostos no Windows
        subprocess.check_call(command, shell=True, cwd=cwd)
        print(f"{Colors.OKGREEN}✅ {description} passou!{Colors.ENDC}")
        return True
    except subprocess.CalledProcessError:
        print(f"{Colors.FAIL}❌ {description} falhou.{Colors.ENDC}")
        return False

def main():
    print(f"{Colors.OKBLUE}--- INICIANDO PRÉ-VALIDAÇÃO DE CI/CD ---{Colors.ENDC}")
    
    # 1. Backend Tests
    if not run_command("python -m pytest", "Testes de Backend (Pytest)"):
        sys.exit(1)

    # 2. Frontend Build (Simulação)
    # Verifica se o frontend compila sem erros de TypeScript
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    if os.path.exists(frontend_dir):
        # Usamos 'npm run build' mas poderíamos usar 'tsc' para ser mais rápido
        # O build garante que não há erros de lint/types que quebrariam a Vercel
        if not run_command("npm run build", "Build do Frontend (Next.js)", cwd=frontend_dir):
            sys.exit(1)
    else:
        print("⚠️ Pasta frontend não encontrada, pulando etapa.")

    print(f"\n{Colors.OKGREEN}🎉 TUDO PRONTO! O código está seguro para subir.{Colors.ENDC}")

if __name__ == "__main__":
    main()
